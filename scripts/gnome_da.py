import datetime
import h5py

from glue.segments import segment
from gwpy.timeseries import TimeSeries
#from pycbc.types import TimeSeries
#
# GNOME specific data retrieval
#

def retrieve_file_paths(base_path, station, gps_start=None, gps_end=None):
    """
    Get all the paths for a given station in a base_path.
    TODO: convert gps segment to UTC and format the path appropriately.
    """
    path_glob = os.path.join(base_path, \
                             "data/GNOMEDrive/gnome/serverdata/%s01/2016/03/23/%s01_20160323_*.hdf5" \
                             % (station, station))
    return glob.glob(path_glob)

def generate_timeseries(data_list, setname="MagneticFields"):
    """
    For each span of time in a dictionary keyed by glue.segment, retrieve the time series for each span. The hdf5 Dataset retrieved is indicated by 'setname' (default: MagneticFields).
    """

    full_data = TimeSeriesList()
    for seg in sorted(data_list):
        hfile = h5py.File(data_list[seg], "r")
        full_data.append(gnome_da.retrieve_data_timeseries(hfile, "MagneticFields"))
        hfile.close()

    return full_data

def retrieve_data_timeseries(hfile, setname):
    """
    Construct a gwpy.timeseries.TimeSeries object from the hdf5 Dataset named in setname. The metadata from the attributes 'SamplingRate(Hz)', 'Date', and 't0' is used to generate time based metadata for the TimeSeries object.
    """
    dset = hfile[setname]
    sample_rate = dset.attrs["SamplingRate(Hz)"]
    gps_epoch = construct_utc_from_metadata(dset.attrs["Date"], dset.attrs["t0"])
    data = retrieve_channel_data(hfile, setname)
    ts_data = TimeSeries(data, sample_rate=sample_rate, epoch=gps_epoch)
    return ts_data

def retrieve_channel_data(hfile, setname):
    """
    Thin wrapper around HDF5 dataset retrieval. NOTE: slicing the full array is equivalent to a copy. This is done because working directly with HDF5 datasets is very slow.
    """
    return hfile[setname][:]

#
# Bookkeeping utilities
#
def _file_to_segment(hfile, segname="MagneticFields"):
    """
    Gerenate a segment (span) of time for which the metadata of a stretch of time is valid.
    """
    attrs = hfile[segname].attrs
    dstr, t0, t1 = attrs["Date"], attrs["t0"], attrs["t1"]
    return segment(construct_utc_from_metadata(dstr, t0), construct_utc_from_metadata(dstr, t1))

#
# Time based utilities
#
def construct_utc_from_metadata(datestr, t0str):
    """
    Format a date string (in a very specific format!) into an ISO datestring and have astropy convert it into a time we can use for GPS conversions.
    """
    instr = "%d-%d-%02dT" % tuple(map(int, datestr.split('/')))
    instr += t0str
    from astropy import time
    t = time.Time(instr, format='isot', scale='utc')
    return t.gps

if False:
    #fname = "data/GNOMEDrive/gnome/serverdata/berkeley01/2016/03/23/berkeley01_20160323_000008.hdf5"
    import glob
    data_order = {}
    for fname in glob.glob("data/GNOMEDrive/gnome/serverdata/berkeley01/2016/03/23/berkeley01_20160323_*.hdf5"):
        hfile = h5py.File(fname, "r")
        data_order[_file_to_segment(hfile)] = hfile

    seglist = segmentlist(data_order.keys())
    seglist.sort()

    # This is just to get metadata
    setname = "MagneticFields"
    ts_data = retrieve_data_timeseries(hfile, setname)
    print ts_data.delta_t, ts_data.start_time

    full_data = numpy.hstack([retrieve_channel_data(data_order[seg], "MagneticFields") for seg in seglist])
    # Zero pad. :(
    zpad = math.ceil(math.log(len(full_data)*ts_data.delta_t, 2))
    zpad = int(2**zpad) - len(full_data)*ts_data.delta_t
    zpad = numpy.zeros(int(zpad/ts_data.delta_t / 2.0))
    full_data = numpy.hstack((zpad, full_data, zpad))
    ts_data = types.TimeSeries(full_data, ts_data.delta_t, epoch=seglist[0][0])

    print ts_data

    for v in data_order.values():
        v.close()
    del data_order
