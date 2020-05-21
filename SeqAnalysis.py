# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 15:19:39 2020

@author: SWannell
"""

import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt; plt.style.use('ggplot')
import matplotlib.ticker as mtick
import pandas as pd


class SeqAnalysis:
    """
    Perform and visualise sequential analysis on split test data.

    ...

    Attributes
    ----------
    z_score: pd.DataFrame
        The cumulative conversions, z-score, and information quotient q by day.
    results: dict
        The cumulative n, conversions, conversion rate, and variance.
        One entry per test cell.
    daily_results: pd.DataFrame
        The daily n, conversions, conversion rate, and variance - by cell.
    figbdr, axbdr: plt items for boundary plot
    figcvr, axcvr: plt items for conversion rate plot
    """
    def __init__(self, target, ttl, data_fp='AmendedData\\CumuData{}.pkl',
                 graph_fp='Outputs\\Results_Target{}.png',
                 alpha=0.05, beta=0.2):
        """
        Initiates the sequential analysis object.

        Parameters
        ----------
        target : int
            The target conversion volume.
        ttl : string
            The title of the boundary graph.
        data_fp : string
            File path of the .pkl data files. One per cell.
        graph_fp : string
            Destination file path of the boundary graph with z_score line.
        """
        self.figbdr, self.axbdr = plt.subplots(1, 1, figsize=(10, 10))
        self.q = np.linspace(0.06, 1, 30)  # information quotient
        self.z_score = self.z_score(target, data_fp)
        self.bdry_plot(alpha, beta)
        self.z_plot(target, ttl, graph_fp)
        self._titledict_ = {'fontsize': 16, 'fontweight': 'bold'}
        self.alpha, self.beta = alpha, beta

    def _obf_bdr_(self, info_q, boundary_param):
        """
        Calculate z-score decision boundary values, using a Lan-Demets spending
        function of O'Brien-Fleming type.

        Parameters
        ----------
        info_q : float, np.array
            The information quotient. All values should be between 0 and 1.
        boundary_param : float
            Could be alpha (e.g. 0.05) or beta (e.g. 0.8).

        Returns
        -------
        f_z : list
            List of z-score boundary values.
        """
        z = norm.ppf(1-boundary_param/2)
        arg = z/np.sqrt(info_q)
        f = 2-2*norm.cdf(arg)  # gives the p-value limit line
        f_z = norm.ppf(f)*-1  # gives the Z-value limit line
        return f_z

    def z_score(self, target, data_fp):
        """
        Calculate the cumulative z-score, using the test data.
        """
        # DFs for each cell
        res = {'ctrl': {}, 'test': {}}
        for cell in res.keys():
            data = pd.read_pickle(data_fp.format(cell))
            data['ctr'] = data['conv'] / data['n']
            data['var'] = data['ctr']*(1-data['ctr'])/data['n']
            res[cell]['by_day'] = data
        self.results = res
        # z-score df
        z_score = pd.DataFrame(index=res['ctrl']['by_day'].index,
                               columns=['n', 'z', 'q'])
        z_num = res['test']['by_day']['ctr'] - res['ctrl']['by_day']['ctr']
        z_var_sq = res['test']['by_day']['var'] + res['ctrl']['by_day']['var']
        z_denom = np.sqrt(z_var_sq)
        z_score['z'] = z_num / z_denom
        z_score['n'] = sum([res[c]['by_day']['conv'] for c in res.keys()])
        z_score['q'] = z_score['n'] / target
        return z_score

    def bdry_plot(self, alpha, beta):
        """
        Plot the z-score boundary lines, with appropriate shading.
        """
        top_line = self._obf_bdr_(self.q, alpha)
        low_line = -top_line
        futil_line = self._obf_bdr_(self.q, beta)*-1

        self.axbdr.plot(self.q, top_line, 'r-', lw=1, alpha=0.7, color='g')
        self.axbdr.plot(self.q, low_line, 'r-', lw=1, alpha=0.7, color='r')
        self.axbdr.plot(self.q, futil_line, 'r-', lw=1, alpha=0.3, color='k')

        self.axbdr.fill_between(self.q, top_line,
                                max(top_line)*np.ones(len(top_line)),
                                color='g', alpha=0.5)
        self.axbdr.fill_between(self.q, low_line,
                                min(low_line)*np.ones(len(low_line)),
                                color='r', alpha=0.5)
        self.axbdr.fill_between(self.q, futil_line, low_line,
                                alpha=0.3, color='k')

    def z_plot(self, target, ttl, graph_fp):
        """
        Plots the z-score boundary lines, with appropriate shading. Saves it.
        """
        titledict = {'fontsize': 16, 'fontweight': 'bold'}
        self.axbdr.plot(self.z_score['q'], self.z_score['z'],
                        color='#000000', marker='.')
        self.axbdr.set_title(ttl, fontdict=titledict)
        self.axbdr.set_xlabel('% recruited')
        self.axbdr.set_ylabel('z-score')
        self.axbdr.xaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
        test_descrip = "Lan-DeMets spending function, O’Brien-Fleming type \
                        boundaries"
        self.figbdr.text(0, 0, test_descrip, color='gray', fontsize=10)
        plt.tight_layout()
        ldm_fp = graph_fp.format(str(target))
        plt.savefig(ldm_fp, bbox_inches="tight")
        plt.show()

    def cvr_plot(self, ttl):
        """
        Calculates and plots the daily and cumulative conversion rate per cell.
        """
        self.figcvr, self.axcvr = plt.subplots(1, 1, figsize=(10, 5))
        colours = {'ctrl': '#1d1a1c', 'test': '#ee2a24'}
        daily = pd.DataFrame()
        for cell in self.results.keys():
            self.axcvr.plot(self.results[cell]['by_day']['ctr'], 'r-', lw=2,
                            color=colours[cell], label=cell+' cumulative')
            daily_cell = self.results[cell]['by_day'].diff()
            daily_cell.iloc[0] = self.results[cell]['by_day'].iloc[0]
            daily_cell['ctr'] = daily_cell['conv'] / daily_cell['n']
            daily_cell['cell'] = cell
            daily_cell.index = self.results['ctrl']['by_day'].index
            daily = pd.concat([daily, daily_cell])
            self.axcvr.plot(daily[daily['cell'] == cell]['ctr'], 'r-', lw=1,
                            color=colours[cell], label=cell+' by day',
                            alpha=0.3)
        self.daily_results = daily
        self.axcvr.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
        self.axcvr.set_ylabel('Opt-in clicks / Form users')
        self.axcvr.set_title(ttl + '\nconversion %', fontdict=self._titledict_)
        for label in self.axcvr.get_xticklabels():
            label.set_rotation(30)
            label.set_ha('right')
        self.axcvr.legend()
        plt.savefig('Outputs\\CTR_by_day.png', bbox_inches="tight")

    def crossed(self):
        """
        Confirm if a boundary has been crossed
        """
        stop_bdr = self.alpha
        futi_bdr = self.beta
        current_q = self.z_score.iloc[-1]['q']
        current_z = self.z_score.iloc[-1]['z']
        current_z_stop = self._obf_bdr_(current_q, stop_bdr)
        current_z_futi = self._obf_bdr_(current_q, futi_bdr)*-1
        print("Current z:", "%.2f" % current_z,
              "\nStop bdry: +/-", "%.2f" % current_z_stop,
              "\nFutility bdry:", "%.2f" % current_z_futi)
        if current_z > abs(current_z_stop):
            print("STOP: z crossed positive boundary. Close test, reject null")
        elif current_z < current_z_futi:
            print("STOP: z crossed futility boundary. Close test, null holds")
        else:
            print("z between boundaries - continue test")

    def summary(self):
        """
        Print the test results, for reports.
        N.B. assumes 'ctrl' and 'test' cells.
        """
        current_z = self.z_score.iloc[-1]['z']
        for cell in self.results.keys():
            for var in ['n', 'conv', 'ctr']:
                _ = self.results[cell]['by_day'][var][-1]
                self.results[cell]['final_{}'.format(var)] = _
            self.results[cell]['final_ctr'] *= 100
            print(cell, "=", "%.0f" % self.results[cell]['final_conv'], "/",
                  "%.0f" % self.results[cell]['final_n'], '=',
                  "%.1f%%" % self.results[cell]['final_ctr'])
        pct_uplift = (self.results['test']['final_ctr'] /
                      self.results['ctrl']['final_ctr'])-1
        print("the test statistic is z= {:.2f}".format(current_z),
              ", p = {:.2f}".format(norm.cdf(current_z)), '\n',
              'the relative % change is ', "%.0f%%" % (pct_uplift*100))
        

# Tests
if __name__ == "__main__":
    two_month_vol, cvr = 3000, 0.214
    target = int(two_month_vol * cvr)
    ttl = 'CR046 email opt-in wording'
    seq = SeqAnalysis(target, ttl)  # returns the plot!!
    seq.cvr_plot(ttl)
    seq.crossed()
    seq.summary()