import alexPlot
import matplotlib.pyplot as plt

def get_ax_1D():
	ax = plt.gca()

	ax.tick_params(axis='both', which='major', labelsize=15)

	return ax

def get_ax_1D_with_pulls():
	ax = plt.axes([0.1, 0.18, 0.8, 0.7])
	ax_pulls = plt.axes([0.1, 0.015, 0.8, 0.07], sharex=ax)
	plt.setp(ax_pulls.get_xticklabels(), visible=False)

	axes = (ax, ax_pulls)
	for axes_i in axes:
		axes_i.tick_params(axis='both', which='major', labelsize=15)

	return ax, ax_pulls

def get_ax_1D_with_pulls_large():
	ax = plt.axes([0.1, 0.28, 0.8, 0.6])
	ax_pulls = plt.axes([0.1, 0.015, 0.8, 0.17], sharex=ax)
	plt.setp(ax_pulls.get_xticklabels(), visible=False)

	axes = (ax, ax_pulls)
	for axes_i in axes:
		axes_i.tick_params(axis='both', which='major', labelsize=15)

	return ax, ax_pulls