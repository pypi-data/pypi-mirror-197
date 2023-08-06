import alexPlot
import zfit
import numpy as np
import matplotlib.pyplot as plt


def plot_1D_PDF(pdf, ax=None, axis='x', normalisation=1., points=1000, switch_axes=False, stack=False,
	colors=None, linewidth=None, plot_components=True, label=None, labels=None, total_pdf_color='r', dash_signal=False, limits=None,
	alpha=None, alphas=None):

	zorder = -100

	# normalisation is for example: yield * binw * sumW /scale2 (most often yield * binw is enough)
	
	if ax == None:
		ax = plt.gca()

	if dash_signal: stack=True
	try: 
		if 'k dashed' in colors: 
			stack = True
	except: 
		pass

	axis = 'x'
	
	if limits is None:
		limits_array = np.asarray(pdf.space.limits)[:,0,:]
		limits = [limits_array[0][0], limits_array[1][0]]
	limits_x = zfit.Space(pdf.obs[0], limits=(limits[0], limits[1]))

	if switch_axes or axis == 'y':
		limits_x, limits_y = limits_y, limits_x

	x = np.linspace(limits[0], limits[1], points)

	# Do this because sum of components != total PDF. Sum of components is more reliable
	total_pdf = np.zeros(np.shape(x))

	if stack:
		y = np.zeros(np.shape(x)) 
		fill_between_min = y

	if isinstance(pdf, zfit.pdf.SumPDF):
		pdf_iterator = zip(pdf.pdfs, pdf.params.values())
	else:
		pdf_iterator = zip([pdf], [1])
		if alpha is not None:
			alphas = [alpha]
		if not stack: plot_components = False

	if plot_components:
		for pdf_idx, (pdf_i, frac_i) in enumerate(pdf_iterator):

			label_i = None
			if labels != None:
				try: label_i = labels[pdf_idx]
				except: label_i = None

			try:
				frac = pdf_i.get_yield().read_value().numpy()/pdf.get_yield().read_value().numpy()
			except:
				try:
					frac = frac_i.read_value().numpy()
				except:
					frac = frac_i

			y = pdf_i.pdf(x) * frac * normalisation
			total_pdf += y

			try:
				color_i = colors[pdf_idx]
			except:
				color_i = None
			try:
				alpha_i = alphas[pdf_idx]
			except:
				alpha_i = 1.

			if stack:
				if colors != None:
					if color_i == 'k dashed' or (pdf_idx == 0 and dash_signal):
						ax.plot(x, y, c='k', linestyle=(0,(1,1)),linewidth=linewidth, label=label_i, zorder=-1)
					else:
						zorder += 1
						if color_i is not None:
							ax.fill_between(x, fill_between_min, fill_between_min+y, alpha=alpha_i, color=color_i, label=label_i, zorder=zorder, linewidth=0)
						else:
							ax.fill_between(x, fill_between_min, fill_between_min+y, alpha=alpha_i, label=label_i, zorder=zorder, linewidth=0)

						fill_between_min += y
				else:
					if pdf_idx == 0 and dash_signal:
						ax.plot(x, y, c='k', linestyle=(0,(1,1)),linewidth=linewidth, label=label_i, zorder=-1, alpha=alpha_i)
					else:
						zorder += 1
						ax.fill_between(x, fill_between_min, fill_between_min+y, label=label_i, zorder=zorder, linewidth=0, alpha=alpha_i)
						fill_between_min += y
			else:
				if colors != None:
					zorder += 1
					if color_i is not None:
						ax.plot(x, y, color=color_i,linewidth=linewidth, label=label_i, zorder=zorder, alpha=alpha_i)
					else:
						ax.plot(x, y,linewidth=linewidth, label=label_i, zorder=zorder, alpha=alpha_i)

				else:
					zorder += 1
					ax.plot(x, y,linewidth=linewidth, label=label_i, zorder=zorder, alpha=alpha_i)


	if not isinstance(pdf, zfit.pdf.SumPDF):
		total_pdf = pdf.pdf(x) * normalisation

	zorder += 1
	if alpha == None: alpha = 1.
	ax.plot(x, total_pdf, c=total_pdf_color,linewidth=linewidth, label=label, zorder=zorder, alpha=alpha)

	ax.set_xlim(limits[0],limits[1])

	return x, total_pdf