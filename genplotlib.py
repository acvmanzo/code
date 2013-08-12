# Library with functions to plot scatter plots and bar graphs.
# Replaces genbarlib.

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import matplotlib
import math


def gendict(fname='peakf.txt'):
    """Generates a dictionary from a file listing the peak frequencies.

    Keywords are the conditions and values are the peak frequencies of each sample for that given
    condition.
    """

    data_dict = {}
    f = open(fname)
    f.next()

    for l in f:
        try:
            name, valuestr, condition = map(str.strip, l.split(','))
        except ValueError:
            name, valuestr, condition = map(str.strip, l.split())

        value = float(valuestr)

        if condition not in data_dict:
            data_dict[condition] = []

        data_dict[condition].append(value)

    return(data_dict)


def gendict_pd(fname, minbin):
    """Generates a dictionary of phase differences from a file listing the phase differences
    and frequencies; use with phaselib.py"""

    data_dict={}
    with open(fname) as f:
        f.next()
        for l in f:
            name, binstr, pdstr, tdstr, fstr, condition = map(str.strip, l.split(','))

            pd, td, f, bin = map(float, [pdstr, tdstr, fstr, binstr])

            if minbin <= bin:
                if condition not in data_dict:
                    data_dict[condition] = []

                data_dict[condition].append(pd)

    return(data_dict)


def gendict_pdl(fname, minbin):
    """Phase dictionary with lengths."""

    data_dict={}
    with open(fname) as f:
        f.next()
        for l in f:
            name, binstr, pdstr, fstr, lstr, condition = map(str.strip, l.split(','))

            pd, f, bin, l = map(float, [pdstr, fstr, binstr, lstr])

            if minbin <= bin:
                if condition not in data_dict:
                    data_dict[condition] = []

                data_dict[condition].append((pd,l))

    return(data_dict)


def gendict_deltaframe(fname):
    data_dict={}
    with open(fname) as f:
        f.next()
        for l in f:
            name, avg_dp, condition = map(str.strip, l.split(','))

            avg_dp = float(avg_dp)

            if condition not in data_dict:
                data_dict[condition] = []

            data_dict[condition].append(avg_dp)

    return(data_dict)


def gendict_deltaphase(fname):
    data_dict={}
    with open(fname) as f:
        f.next()
        for l in f:
            name, avg_dp, condition = map(str.strip, l.split(','))

            avg_dp = float(avg_dp)

            if condition not in data_dict:
                data_dict[condition] = []

            data_dict[condition].append(avg_dp)

    return(data_dict)




def gendict_freq(fname, minbin):
    """Generates a dictionary of frequencies from a file listing the phase differences
    and frequencies; use with phaselib.py"""

    data_dict={}
    with open(fname) as f:
        f.next()
        for l in f:
            name, binstr, tdstr, pdstr, fstr, condition = map(str.strip, l.split(','))

            pd, td, f, bin = map(float, [pdstr, tdstr, fstr, binstr])
            if minbin <= bin:

                if condition not in data_dict:
                    data_dict[condition] = []

                data_dict[condition].append(f)

    return(data_dict)


def gendict_td(fname, minbin):
    """Generates a dictionary of time delays from a file listing the phase differences
    and frequencies; use with phaselib.py"""

    data_dict={}
    with open(fname) as f:
        f.next()
        for l in f:
            name, binstr, pdstr, tdstr, fstr, condition = map(str.strip, l.split(','))

            pd, td, f, bin = map(float, [pdstr, tdstr, fstr, binstr])
            if minbin <= bin:

                if condition not in data_dict:
                    data_dict[condition] = []

                data_dict[condition].append(td)

    return(data_dict)


def gendict_phase(fname, value):

    data_dict={}
    with open(fname) as f:
        f.next()
        for l in f:
            name, df, st_df, dt, st_dt, dp, freq, condition = map(str.strip, l.split(','))

            df, st_df, dt, st_dt, dp, freq = map(float, [df, st_df, dt, st_dt, dp, freq])

            dpftup = (dp, freq)

            if condition not in data_dict:
                data_dict[condition] = []

            if value == 'deltaframe':
                data_dict[condition].append(df)

            if value == 'deltatime':
                data_dict[condition].append(dt)

            if value == 'deltaphase':
                data_dict[condition].append(dp)

            if value == 'peakf':
                data_dict[condition].append(peakf)

            if value == 'dp_freq':
                data_dict[condition].append(dpftup)

    return(data_dict)


def gendict_cibarea_fracopen(fname):

    data_dict={}
    with open(fname) as f:
        f.next()
        for l in f:
            name, fracopenstr, durstr, condition = map(str.strip, l.split(','))

            try:
                fracopen = float(fracopenstr)
                if condition not in data_dict:
                    data_dict[condition] = []

                data_dict[condition].append(fracopen)

            except ValueError:
                continue


    return(data_dict)


def gendict_cibarea_dur(fname):

    data_dict={}
    with open(fname) as f:
        f.next()
        for l in f:
            name, fracopenstr, durstr, condition = map(str.strip, l.split(','))

            try:
                dur = float(durstr)

                if condition not in data_dict:
                    data_dict[condition] = []

                data_dict[condition].append(dur)

            except ValueError:
                continue


    return(data_dict)

def gendict_volperpump(fname):
    data_dict={}
    with open(fname) as f:
        f.next()
        for l in f:
            name, nlpersec, peakf, volperpump, condition = map(str.strip, l.split(','))

            nlpersec, peakf, volperpump = map(float, [nlpersec, peakf, volperpump])

            if condition not in data_dict:
                data_dict[condition] = []

            data_dict[condition].append(volperpump)

    return(data_dict)


def gendict_cibgf(fname):

    dmean = {}
    ddiffa = {}

    with open(fname) as f:
        f.next()
        for l in f:
            fly, mov24, mov32, mean24, mean32, diffa, condition = map(str.strip, l.split(','))

            mean24, mean32, diffa = map(float, [mean24, mean32, diffa])
            #print(mean24, mean32, diffa)

            if condition + ' - 24' not in dmean:
                dmean[condition + ' - 24'] = []
                dmean[condition + ' - 32'] = []

            if condition not in ddiffa:
                ddiffa[condition] = []

            dmean[condition + ' - 24'].append(mean24)
            dmean[condition + ' - 32'].append(mean32)
            ddiffa[condition].append(diffa)

    return(dmean, ddiffa)





def genlist(dict, label='data'):
    """Generates a new dictionary in which the keywords are conditions and the values are lists of
    the mean frequency, standard deviation, standard error, and n for that condition.
    """

    mean_dict = {}

    for condition, value in dict.iteritems():
        print(condition)
        meanval = np.mean(value)
        stdev = np.std(value)
        n = len(value)
        sterr = stdev/np.sqrt(n)

        if condition not in mean_dict:
            mean_dict[condition] = []

        mean_dict[condition].append(meanval)
        mean_dict[condition].append(stdev)
        mean_dict[condition].append(sterr)
        mean_dict[condition].append(n)
        mean_dict[condition].append('{0}'.format(label))


    return(mean_dict)


def genalldict(fname='peakf.txt'):
    """Generates two dictionaries: in the first, the keywords are conditions and the values are the
    data points, and in the second, the values are lists of the mean frequency, std dev, std
    error, and n for each condition.
    """

    d = gendict(fname)
    md = genlist(d)
    return(d, md)



def genkeylist(dict):
    i = dict.keys()
    i = sorted(i)
    return(i)



def savebar(fname = 'bargraph'):
    """Saves the bar graph plotted with 'plotbar'."""
    plt.savefig(fname)





def plotdata(dictdata, dictmeans, keylist, ptype, ylabel, ftitle, datac='b', meanc='r',
bcolor='k', withleg='no', err='sterr', xd=1, xstart=0, xtoffset=0, end=1, titlesize='xx-large', xlabelsize='large'):
    """Plots either a bar graph or a scatter plot using data from 'dictdata', with means taken from 'dictmeans' in the
    order specified by 'keylist'.

    ptype = ['b' | 's']
        b: bar graph
        s: scatter plot
        bw: box and whisker plot

    ylabel = label for the yaxis
    ftitle = title of the figure
    ylim = limit of y axis
    datac = color of data points
    meanc = color of point representing the mean value
    bcolor = color of bars
    withleg = [yes]
        yes: legend displayed; otherwise, no legend displayed
    err = ['stderr' | 'stdev']
        Plot standard error or standard deviation.
    xd = the distance between data points on the x-axis
    xstart is the distance from zero to the first set of data points on the x-axis.
    xtoffset is the distance between the labels on the x-axis.

    Start and xtoffset can be changed to provide the appropriate spacing for the data points along the
    x-axis. Also, if two sets of data are to be plotted using the same x-axis labels, start and
    xtoffset can be changed so that the two sets of data share the same labels.
    """

    i = keylist
    num = len(dictdata)
    x = xstart

    x_list = []
    cond_list = []
    dataxvals = []
    datayvals = []
    bwyvals = []
    meanyvals = []
    meanstdev = []
    meansterr = []


    fig1 = plt.figure()

    for condition in i:

        # 'datayvals' is a list of the data points.

        data = dictdata[condition]
        datayvals.extend(data)

        # 'dataxvals' is a list of the xvalues for each data point.
        x = x+xd
        xv = np.tile(x, len(data)).tolist()
        dataxvals.extend(xv)

        # 'bwyvals' is a list of lists containing the data points.

        bwyvals.append(dictdata[condition])


        # 'meanyvals' is a list of the mean values for each condition, 'meanstdev' is a list of
        # the standard deviations for each condition, and 'meansterr' is a list of the standard errors
        # for each condition.
        mean, stdev, sterr, n, label = dictmeans[condition]
        meanyvals.append(mean)
        meanstdev.append(stdev)
        meansterr.append(sterr)

        # 'x_list' is a list of the xvalues for each condition.
        x_list.append(x)

        # If the length of the condition name is too long, this adds a line break at the first
        # space in the condition name for so that it looks better as an xlabel in the graph.
        if len(condition) > 40:
            formcondition = condition.replace(' ', '\n', 1)
        else:
            formcondition = condition
        #Uncomment this line to show include the n in the x-axis label.
        cond_list.append(formcondition + '\n' + 'n=' + str(n))

        #Uncomment this line to not include the n in the x-axis label.
        #cond_list.append(formcondition)

    if ptype == 'b':
        if err == 'sterr':
            plt.bar(x_list, meanyvals, width=0.5, color=bcolor, yerr=meansterr, ecolor=bcolor, label=label)
        if err == 'stdev':
            plt.bar(x_list, meanyvals, width=0.5, color=bcolor, yerr=meanstdev, ecolor=bcolor, label=label)
        if err == 'none':
            plt.bar(x_list, meanyvals, width=0.5, color=bcolor, ecolor=bcolor, label=label)
        xtoffset = xtoffset + 0.25
        #This line specifies the x and y limits; modify as needed.
        #plt.axis([0.5, num+end, ymin, ylim])
        plt.xlim(0.5, num+end)

    if ptype == 's':

        # Plots the data as points.
        # Uncomment this line if you want the label to just include the label in the dictmeans
        # dictionary.
        plt.scatter(dataxvals, datayvals, c=datac, marker='s', label=label)

        #Uncomment these lines if you want the label to include the condition and the n.
        #plt.scatter(dataxvals, datayvals, c=datac, marker='s', label=condition + ', ' +
        #label + ', n = {0}'.format(n))

        # Plots the mean values and the error bar.
        if err == 'sterr':
            plt.errorbar(x_list, meanyvals, meansterr, mfc=meanc, mec=meanc, ecolor=meanc, ms=7,
            elinewidth=2, barsabove='True', capsize=8, fmt='o')
        if err == 'stdev':
            plt.errorbar(x_list, meanyvals, meanstdev, mfc=meanc, mec=meanc, ecolor=meanc, ms=7,
            elinewidth=2, barsabove='True', capsize=8, fmt='o')

        #This line specifies the x and y limits; modify as needed.
        #plt.axis([0.5, num+end, ymin, ylim])
        plt.xlim(0.5, num+end)

    if ptype == 'bw':
        plt.boxplot(bwyvals)
        plt.xlim(0.5, num+end)


    #xt specifies the x values for the x-axis labels.
    xt = [n+xtoffset for n in x_list]



    #If the length of the labels are > 25, then the labels are rotated.
    cond_list_len = [len(c) for c in cond_list]
    if max(cond_list_len) > 15:
        plt.xticks(xt, cond_list, rotation=90, fontsize=xlabelsize)
        fig1.subplots_adjust(bottom=0.35)

    else:
        plt.xticks(xt, cond_list, fontsize=xlabelsize)




    plt.ylabel(ylabel, fontsize='x-large')
    plt.ftitle(ftitle, fontsize=titlesize)

    if withleg == 'yes':
        leg = plt.legend(loc='best', scatterpoints=1)
        for t in leg.get_texts():
            t.set_fontsize('medium')
    plt.draw()
    return(fig1)


def plot_phaseplot(dictdata, keys, autok, title, withn='yes'):
    """Plots a phase plot where the radius is fixed at 1"""

    colors = ['r', 'b', 'g', 'y', 'k']

    if autok == 'yes':
        k = dictdata.keys()

    plt.suptitle(title, fontsize='large' )

    for i, condition in enumerate(keys):
    #for i, condition in enumerate(iter(dictdata)):
        data = dictdata[condition]
        datac = colors[i]
        try:
            n = len(data)
            theta = []
            theta.extend(data)
            r1 = 1
            r = np.repeat(r1, n)

        except TypeError:
            r = 1
            theta = data
            n = 1

        if withn == 'yes':
            plt.polar(theta, r, 'o', color=datac, label=condition + '\n n=' + str(n))
        if withn == 'no':
            plt.polar(theta, r, 'o', color=datac, label=condition)

        lines, labels = plt.rgrids( (0.5, 1.0), ('', ''), angle=0 )
        tlines, tlabels = plt.thetagrids( (0, 90, 180, 270), ('0', 'pi/2', 'pi', '3pi/2') )
        leg = plt.legend(loc='center')
        for t in leg.get_texts():
            t.set_fontsize('small')

        plt.subplots_adjust(top=0.85)
        plt.draw()


def plotdata_ci(dictdata, dictpercent, keylist, ptype, ylabel, ftitle, ymin=-5, ylim=100, datac='b', meanc='r',
bcolor='k', withleg='no', err='sterr', xd=1, xstart=0, xtoffset=0, end=1, titlesize='xx-large', xlabelsize='large'):
    """Plots either a bar graph or a scatter plot using data from 'dictdata', with means taken from 'dictmeans' in the
    order specified by 'keylist'.

    ptype = ['b' | 's']
        b: bar graph
        s: scatter plot

    ylabel = label for the yaxis
    ftitle = title of the figure
    ylim = limit of y axis
    datac = color of data points
    meanc = color of point representing the mean value
    bcolor = color of bars
    withleg = [yes]
        yes: legend displayed; otherwise, no legend displayed
    err = ['stderr' | 'stdev']
        Plot standard error or standard deviation.
    xd = the distance between data points on the x-axis
    xstart is the distance from zero to the first set of data points on the x-axis.
    xtoffset is the distance between the labels on the x-axis.

    Start and xtoffset can be changed to provide the appropriate spacing for the data points along the
    x-axis. Also, if two sets of data are to be plotted using the same x-axis labels, start and
    xtoffset can be changed so that the two sets of data share the same labels.
    """

    i = keylist
    num = len(dictdata)
    x = xstart

    x_list = []
    cond_list = []
    dataxvals = []
    datayvals = []
    percentyvals = []
    lcivals = []
    ucivals = []

    fig1 = plt.figure()

    for condition in i:
        # 'datayvals' is a list of the data points.
        data = dictdata[condition]
        datayvals.extend(data)

        # 'dataxvals' is a list of the xvalues for each data point.
        x = x+xd
        xv = np.tile(x, len(data)).tolist()
        dataxvals.extend(xv)

        # 'meanyvals' is a list of the mean values for each condition, 'meanstdev' is a list of
        # the standard deviations for each condition, and 'meansterr' is a list of the standard errors
        # for each condition.
        prop, lci, uci, nsuccess, n = dictpercent[condition] # num = # of successes; n = total
        prop, lci, uci, nsuccess, n = map(float, [prop, lci, uci, num, n])
        percent = 100*prop
        lci = 100*lci
        uci = 100*uci

        percentyvals.append(percent)
        lcivals.append(lci)
        ucivals.append(uci)

        label = condition


        # 'x_list' is a list of the xvalues for each condition.
        x_list.append(x)

        # If the length of the condition name is too long, this adds a line break at the first
        # space in the condition name for so that it looks better as an xlabel in the graph.
        if len(condition) > 20:
            formcondition = condition.replace(' ', '\n', 1)
        else:
            formcondition = condition
        #Uncomment this line to show include the n in the x-axis label.
        cond_list.append(formcondition + '\n' + 'n=' + str(n))

        #Uncomment this line to not include the n in the x-axis label.
        #cond_list.append(formcondition)



    if ptype == 'b':
        xtoffset = xtoffset + 0.25
        #xt specifies the x values for the x-axis labels.
        xt = [n+xtoffset for n in x_list]

        print(lcivals)
        print(ucivals)
        plt.bar(x_list, percentyvals, width=0.5, color=bcolor, ecolor=bcolor, label=condition)
        plt.errorbar(xt, percentyvals, yerr=[lcivals,ucivals], fmt=None, ecolor='r')


        #This line specifies the x and y limits; modify as needed.
        plt.axis([0.5, num+1, ymin, ylim])

    if ptype == 's':

        # Plots the data as points.
        # Uncomment this line if you want the label to just include the label in the dictmeans
        # dictionary.
        plt.scatter(dataxvals, datayvals, c=datac, marker='s', label=label)

        #Uncomment these lines if you want the label to include the condition and the n.
        #plt.scatter(dataxvals, datayvals, c=datac, marker='s', label=condition + ', ' +
        #label + ', n = {0}'.format(n))

        # Plots the mean values and the error bar.
        plt.errorbar(x_list, percentyvals, yerr=[lcivals,ucivals], mfc=meanc, mec=meanc, ecolor=meanc, ms=7,
            elinewidth=2, barsabove='True', capsize=8, fmt='o')

        #This line specifies the x and y limits; modify as needed.
        plt.axis([0.5, num+end, ymin, ylim])

        #xt specifies the x values for the x-axis labels.
        xt = [n+xtoffset for n in x_list]



    #If the length of the labels are > 25, then the labels are rotated.
    cond_list_len = [len(c) for c in cond_list]
    if max(cond_list_len) > 20:
        plt.xticks(xt, cond_list, rotation=90, fontsize=xlabelsize)
    else:
        plt.xticks(xt, cond_list, fontsize=xlabelsize)


    plt.ylabel(ylabel, fontsize='x-large')
    plt.title(ftitle, fontsize=titlesize)

    if withleg == 'yes':
        leg = plt.legend(loc='best', scatterpoints=1)
        for t in leg.get_texts():
            t.set_fontsize('medium')
    plt.draw()

    return(fig1)


def plot_phaseplot(dictdata, keys, autok, title, withn='yes'):
    """Plots a phase plot where the radius is fixed at 1"""

    colors = ['r', 'b', 'g', 'y', 'k']

    if autok == 'yes':
        k = dictdata.keys()

    plt.suptitle(title, fontsize='large' )

    for i, condition in enumerate(keys):
    #for i, condition in enumerate(iter(dictdata)):
        data = dictdata[condition]
        datac = colors[i]
        try:
            n = len(data)
            theta = []
            theta.extend(data)
            r1 = 1
            r = np.repeat(r1, n)

        except TypeError:
            r = 1
            theta = data
            n = 1

        if withn == 'yes':
            plt.polar(theta, r, 'o', color=datac, label=condition + '\n n=' + str(n))
        if withn == 'no':
            plt.polar(theta, r, 'o', color=datac, label=condition)

        lines, labels = plt.rgrids( (0.5, 1.0), ('', ''), angle=0 )
        tlines, tlabels = plt.thetagrids( (0, 90, 180, 270), ('0', 'pi/2', 'pi', '3pi/2') )
        leg = plt.legend(loc='center')
        for t in leg.get_texts():
            t.set_fontsize('small')

        plt.subplots_adjust(top=0.85)
        plt.draw()


def plot_phaseplot_l(dictdata, keys, autok, title, withn='yes'):
    """Plots a phase plot where the radius is not fixed to 1."""

    colors = ['r', 'b', 'g', 'y', 'k']

    plt.suptitle(title, fontsize='large' )
    if autok == 'yes':
        k = dictdata.keys()

    for i, condition in enumerate(keys):
        datac = colors[i]
        data = dictdata[condition]

        try:
            n = len(data)
            theta, r = zip(*data)
        except TypeError:
            theta, r = data
            n = 1
        if withn == 'yes':
            plt.polar(theta, r, 'o', color=datac, label=condition + '\n n=' + str(n))
        if withn == 'no':
            plt.polar(theta, r, 'o', color=datac, label=condition)

        lines, labels = plt.rgrids( (1.0, 1.4), ('', ''), angle=0 )
        tlines, tlabels = plt.thetagrids( (0, 90, 180, 270), ('0', 'pi/2', 'pi', '3pi/2') )
        leg = plt.legend(loc=(0.93,0.8))

        for t in leg.get_texts():
            t.set_fontsize('small')

        plt.subplots_adjust(top=0.85)
        plt.draw()


def plot_phaseplot_lpf(dictdata, keys, autok, title, withn='yes'):
    colors = ['r', 'b', 'g', 'y', 'k']

    plt.suptitle(title, fontsize='large' )
    if autok == 'yes':
        k = dictdata.keys()

    for i, condition in enumerate(keys):
        datac = colors[i]
        data = dictdata[condition]

        try:
            n = len(data)
            theta, r = zip(*data)
        except TypeError:
            theta, r = data
            n = 1
        if withn == 'yes':
            plt.polar(theta, r, 'o', color=datac, label=condition + '\n n=' + str(n))
        if withn == 'no':
            plt.polar(theta, r, 'o', color=datac, label=condition)

        #lines, labels = plt.rgrids( (1.0, 1.4), ('', ''), angle=0 )
        tlines, tlabels = plt.thetagrids( (0, 90, 180, 270), ('0', 'pi/2', 'pi', '3pi/2') )
        leg = plt.legend(loc=(0.95,0.75))

        for t in leg.get_texts():
            t.set_fontsize('small')

        plt.subplots_adjust(top=0.85)
        plt.draw()



#def plotdatac(dictdata, dictmeans, keylist, ptype, ylabel, ftitle, ymin=0, ylim=10, datac='b', meanc='r',
#bcolor='k', withleg='no', xd=1, xstart=0, xtoffset=0, end=1, lw=1):
    #"""Plots either a bar graph or a scatter plot using data from 'dictdata', with means taken from 'dictmeans' in the
    #order specified by 'keylist'.

    #ptype = ['b' | 's']
        #b: bar graph
        #s: scatter plot

    #ylabel = label for the yaxis
    #ftitle = title of the figure
    #ylim = limit of y axis
    #datac = color of data points
    #meanc = color of point representing the mean value
    #bcolor = color of bars
    #withleg = [yes]
        #yes: legend displayed; otherwise, no legend displayed
    #xd = the distance between data points on the x-axis
    #xstart is the distance from zero to the first set of data points on the x-axis.
    #xtoffset is the distance between the labels on the x-axis.

    #Start and xtoffset can be changed to provide the appropriate spacing for the data points along the
    #x-axis. Also, if two sets of data are to be plotted using the same x-axis labels, start and
    #xtoffset can be changed so that the two sets of data share the same labels.
    #"""

    #matplotlib.rc('grid', linewidth=2)


    #i = keylist
    #num = len(dictdata)
    #x = xstart

    #x_list = []
    #cond_list = []
    #dataxvals = []
    #datayvals = []
    #meanyvals = []
    #meanstdev = []
    #meansterr = []

    #for condition in i:
        ## 'datayvals' is a list of the data points.
        #data = dictdata[condition]
        #datayvals.extend(data)

        ## 'dataxvals' is a list of the xvalues for each data point.
        #x = x+xd
        #xv = np.tile(x, len(data)).tolist()
        #dataxvals.extend(xv)

        ## 'meanyvals' is a list of the mean values for each condition, 'meanstdev' is a list of
        ## the standard deviations for each condition, and 'meansterr' is a list of the standard errors
        ## for each condition.
        #mean, stdev, sterr, n, label = dictmeans[condition]
        #meanyvals.append(mean)
        #meanstdev.append(stdev)
        #meansterr.append(sterr)

        ## 'x_list' is a list of the xvalues for each condition.
        #x_list.append(x)

        ## If the length of the condition name is too long, this adds a line break at the first
        ## space in the condition name for so that it looks better as an xlabel in the graph.
        #if len(condition) > 15:
            #formcondition = condition.replace(' ', '\n', 1)
        #else:
            #formcondition = condition
        ##Uncomment this line to show include the n in the x-axis label.
        #cond_list.append(formcondition + '\n' + 'n=' + str(n))

        ##Uncomment this line to not include the n in the x-axis label.
        ##cond_list.append(formcondition)

    #if ptype == 'b':
        #plt.bar(x_list, meanyvals, width=0.5, color=bcolor, yerr=sterr, ecolor=bcolor, label=label)
        #xtoffset = xtoffset + 0.25
        ##This line specifies the x and y limits; modify as needed.
        #plt.axis([0.5, num+1, ymin, ylim])

    #if ptype == 's':

        ## Plots the data as points.
        ## Uncomment this line if you want the label to just include the label in the dictmeans
        ## dictionary.
        #ax = plt.scatter(dataxvals, datayvals, c=datac, marker='s', lw=lw, label=label)

        ##Uncomment these lines if you want the label to include the condition and the n.
        ##plt.scatter(dataxvals, datayvals, c=datac, marker='s', label=condition + ', ' +
        ##label + ', n = {0}'.format(n))

        ## Plots the mean values and the error bar.
        #plt.errorbar(x_list, meanyvals, meansterr, mfc=meanc, mec=meanc, ecolor=meanc, ms=7, fmt='o')

        ##This line specifies the x and y limits; modify as needed.
        #plt.axis([0.5, num+end, 0, ylim])


    ##xt specifies the x values for the x-axis labels.
    #xt = [n+xtoffset for n in x_list]

    ##If the length of the labels are > 25, then the labels are rotated.
    #cond_list_len = [len(c) for c in cond_list]
    #if max(cond_list_len) > 30:
        #plt.xticks(xt, cond_list, rotation=17, fontsize='x-large')
    #else:
        #plt.xticks(xt, cond_list, fontsize='x-large')


    #plt.ylabel(ylabel, fontsize='x-large')
    #plt.title(ftitle, fontsize='xx-large')

    #if withleg == 'yes':
        #leg = plt.legend(loc='best', scatterpoints=1)
        #for t in leg.get_texts():
            #t.set_fontsize('medium')


def plotpvalue(sample1, sample2, xtext, ytext):

    t, p = stats.ttest_ind(sample1, sample2)
    pvaltext = 'p-value = {0:.4f}'.format(p)
    bbox_props = dict(boxstyle="square,pad=0.3", fc="white", ec="k", lw=1)
    plt.text(xtext, ytext, pvaltext, bbox=bbox_props)



def var_str(name, value):
    return 'c' + name + ' = ' + value + '\n'


def genpeakfile(dict):
    """Generates an m file where each line is the following format:
    condition = [list of peak frequency values].
    Dictionary should be the output of gendict.
    """

    f = open(('peakf.m'), 'w')

    for condition, value in dict.iteritems():
        f.write(var_str(condition, str(value).replace(',','')))



def checksig(dict):
    """Returns one list of all the values in the dictionary.
    """

    sorted(dict.items())
    num = len(dict)

    cond_list = []

    i = dict.iteritems()
    i = sorted(i)

    m = []

    for condition, value in i:
        m.append(value)

    return(m)


def gendictper(fname):
    """Returns a dictionary made from the filename 'fname'. The keyword is the entry in the
    first column, and the value is the entry in the second column.
    """

    data_dict = {}
    f = open(fname)
    f.next()

    for l in f:
        condition = l.split(',')[0]
        valuestr = l.split(',')[1].strip('\n')

        value = float(valuestr)

        if condition not in data_dict:
            data_dict[condition] = []

        data_dict[condition].append(value)

    return(data_dict)



def genfilepercent(fname, newfile):
    """For calculating the % of flies that can pump."""

    with open(newfile, 'w') as g:
        g.write('Movie,Success?,Condition\n')
        g.close()

    f = open(fname)
    f.next()

    for l in f:
        try:
            name, valuestr, condition = map(str.strip, l.split(','))
            value = float(valuestr)
        except ValueError:
            name, condition, valuestr = map(str.strip, l.split(','))
            value = float(valuestr)

        if value > 0:
            newval = 1

        if value ==0:
            newval = 0

        with open(newfile, 'a') as g:
            g.write('{0},{1},{2}\n'.format(name, newval, condition))


def removezerovalues(fname, newfile):
    """Generates a new file where lines with a pump value of zero have been removed."""

    with open(newfile, 'w') as g:
        g.write('Movie,Pumpfreq,Condition\n')
        g.close()

    f = open(fname)
    f.next()

    for l in f:
        name, valuestr, condition = map(str.strip, l.split(','))

        value = float(valuestr)

        if value ==0:
            continue

        with open(newfile, 'a') as g:
            g.write('{0},{1},{2}\n'.format(name, value, condition))


def printpeakf(fname='peakf.txt'):
    """Prints each line in the document 'fname'."""

    f = open(fname)
    for l in f:
        print(l)


def gendictper2(fname):
    """Generates a dictionary from a file listing the peak frequencies.

    Keywords are the conditions and values are the peak frequencies of each sample for that given
    condition.
    """

    data_dict = {}
    f = open(fname)
    f.next()

    for l in f:
        try:
            condition, valuestr = map(str.strip, l.split(','))
        except ValueError:
            name, condition, valuestr = map(str.strip, l.split(','))

        value = float(valuestr)

        if condition not in data_dict:
            data_dict[condition] = []

        data_dict[condition].append(value)

    return(data_dict)


def gendict1val(fname):
    """Generates a dictionary from a file listing the peak frequencies.

    Keywords are the conditions and values are the peak frequencies of each sample for that given
    condition.
    """

    data_dict = {}
    f = open(fname)
    f.next()

    for l in f:
        name, valuestr, condition = map(str.strip, l.split(','))

        value = float(valuestr)

        if condition not in data_dict:
            data_dict[condition] = []

        data_dict[condition].append(value)

    return(data_dict)



def plot_phase_freq(dictdata, title, ymin=0, ylim=8, datac='b', meanc='r', bcolor='k', withleg='no'):
    """Plots a scatter plot of phase vs. frequency for each condition.

    ylabel = label for the yaxis
    ftitle = title of the figure
    ylim = limit of y axis
    datac = color of data points
    meanc = color of point representing the mean value
    bcolor = color of bars
    withleg = [yes]
        yes: legend displayed; otherwise, no legend displayed
    """

    fighandles = []

    for i, condition in enumerate(iter(dictdata)):

        b = plt.figure()
        fighandles.append(b)

        data = dictdata[condition]
        plt.suptitle(title + condition, fontsize='x-large' )
        plt.ylabel('Frequency', fontsize='x-large')
        plt.xlabel('Phase', fontsize='x-large')

        for datum in data:
            #print(datum)
            plt.scatter(*datum, c=datac, marker='s', label=condition)

        #This line specifies the x and y limits; modify as needed.
        plt.axis([-2*np.pi, 2*np.pi, ymin, ylim])

    return(fighandles)

        #Uncomment these lines if you want the label to include the condition and the n.
        #plt.scatter(dataxvals, datayvals, c=datac, marker='s', label=condition + ', ' +
        #label + ', n = {0}'.format(n))

    #if withleg == 'yes':
        #leg = plt.legend(loc='best', scatterpoints=1)
        #for t in leg.get_texts():
            #t.set_fontsize('medium')


def plot_phase_freq_oneplot(dictdata, keys, title, markersize, ymin=0, ylim=8, datac='b', meanc='r', bcolor='k', withleg='no'):

    colors = ['r', 'b', 'g', 'y', 'k']
    plt.suptitle(title, fontsize='x-large' )

    for i, condition in enumerate(keys):
    #for i, condition in enumerate(iter(dictdata)):

        data = dictdata[condition]
        xdata, ydata = zip(*data)
        n = str(len(xdata))

        ##plt.suptitle(title + condition, fontsize='x-large' )
        plt.ylabel('Frequency', fontsize='x-large')
        plt.xlabel('Phase', fontsize='x-large')

        datac = colors[i]

        #for datum in data[0]:
            #print(datum)
        plt.scatter(xdata, ydata, c=datac, edgecolor=datac, marker='s', s=markersize, label=condition + '\n n=' + n)

        #for datum in data[1:]:
            #plt.scatter(*datum, c=datac, marker='s')

        #This line specifies the x and y limits; modify as needed.
    plt.axis([-2*np.pi, 2*np.pi, ymin, ylim])
    leg = plt.legend(loc='best')

    for t in leg.get_texts():
        t.set_fontsize('small')


def gendictgc(fname):
    # Returns three dictionaries, one containing data for the peak deltaf/f, one for the area of the response, and one for the duration of the response.

    peakd = {}
    aread = {}
    durd = {}

    with open(fname) as f:
        f.next()
        for l in f:
            movie, tastant, fps, zmotion, neurons, peak, area, dur, dfthreshold = map(str.strip, l.split(','))
            fps, zmotion, neurons, peak, area, dur, dfthreshold = map(float, [fps, zmotion, neurons, peak, area, dur, dfthreshold])

            ds = zip([peakd, aread, durd], [peak, area, dur])
            for d in ds:
                if tastant not in d[0]:
                    d[0][tastant] = []

                d[0][tastant].append(d[1])

    return([peakd, aread, durd])

def gendictgc2(fname):

    peakd = {}
    aread = {}
    durd = {}
    dyearead = {}

    with open(fname) as f:
        f.next()
        for l in f:
            movie, tastant, fps, zmotion, neurons, peak, area, dur, dfthreshold, dyearea = map(str.strip, l.split(','))
            fps, zmotion, neurons, peak, area, dur, dfthreshold, dyearea = map(float, [fps,
            zmotion, neurons, peak, area, dur, dfthreshold, dyearea])

            ds = zip([peakd, aread, durd, dyearead], [peak, area, dur, dyearea])
            for d in ds:
                if tastant not in d[0]:
                    d[0][tastant] = []

                d[0][tastant].append(d[1])

    return([peakd, aread, durd, dyearead])
