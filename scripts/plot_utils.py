def plot_ts(ts, fname="ts.png"):
    import matplotlib
    matplotlib.use("agg")
    from matplotlib import pyplot

    from gwpy.plotter import TimeSeriesPlot
    from gwpy.timeseries import TimeSeries
    plot = TimeSeriesPlot()
    ax = plot.gca()
    ax.plot(TimeSeries(ts, sample_rate=1.0/ts.delta_t, epoch=ts.start_time))
    pyplot.savefig(fname)
    pyplot.close()

def plot_spectrum(fd_psd):
    import matplotlib
    matplotlib.use("agg")
    from matplotlib import pyplot

    from gwpy.plotter import SpectrumPlot
    from gwpy.spectrum import Spectrum
    plot = SpectrumPlot()
    ax = plot.gca()
    ax.plot(Spectrum(fd_psd, df=fd_psd.delta_f))
    #pyplot.ylim(1e-10, 1e-3)
    pyplot.xlim(0.1, 500)
    pyplot.loglog()
    pyplot.savefig("psd.png")
    pyplot.close()

def plot_spectrogram(spec, fname="specgram.png"):
    import matplotlib
    matplotlib.use("agg")
    from matplotlib import pyplot

    from gwpy.spectrogram import Spectrogram
    from gwpy.plotter import SpectrogramPlot
    plot = SpectrogramPlot()
    ax = plot.gca()
    ax.plot(Spectrogram(spec), cmap='viridis')
    plot.add_colorbar()
    #pyplot.ylim(1e-9, 1e-2)
    #pyplot.xlim(0.1, 500)
    #pyplot.loglog()
    pyplot.savefig(fname)
    pyplot.close()

def plot_spectrogram_from_ts(ts):
    import matplotlib
    matplotlib.use("agg")
    from matplotlib import pyplot

    from gwpy.spectrogram import Spectrogram
    from gwpy.plotter import SpectrogramPlot
    plot = SpectrogramPlot()
    ax = plot.gca()
    ax.plot(Spectrogram(spec))
    #pyplot.ylim(1e-9, 1e-2)
    #pyplot.xlim(0.1, 500)
    #pyplot.loglog()
    pyplot.savefig("specgram.png")
    pyplot.close()
