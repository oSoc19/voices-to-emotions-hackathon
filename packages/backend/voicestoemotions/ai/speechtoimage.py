import matplotlib.pyplot as plt
import librosa
import librosa.display as ldisplay
import numpy


def create_spectrogram(filename):
    plt.interactive(False)
    clip, sample_rate = librosa.load(filename, sr=None)
    fig = plt.figure(figsize=[0.72, 0.72])
    ax = fig.add_subplot(111)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.set_frame_on(False)
    S = librosa.feature.melspectrogram(y=clip, sr=sample_rate)
    ldisplay.specshow(librosa.power_to_db(S, ref=numpy.max))
    filename = filename.replace('.wav', '.png')
    plt.savefig(filename, dpi=400, bbox_inches='tight', pad_inches=0)
    plt.close()
    fig.clf()
    plt.close(fig)
    plt.close('all')
    del clip, sample_rate, fig, ax, S
    return filename
