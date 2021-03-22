# This file is part of alpaca.

# alpaca is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# alpaca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with alpaca.  If not, see <https://www.gnu.org/licenses/>.

# Copyright (C) 2021 Udo Friman-Gayer

import matplotlib.pyplot as plt
import numpy as np

from .analyzing_power import AnalyzingPower
from .angular_correlation import AngularCorrelation
from .level_scheme_plotter import LevelSchemePlotter
from .state import State
from .transition import Transition


class AnalyzingPowerPlotter:
    def __init__(
        self,
        angular_correlation,
        delta_values,
        convention="natural",
        theta_1=0.5 * np.pi,
        theta_1_label=r"90^\circ",
        theta_2=0.25 * np.pi,
        theta_2_label=r"45^\circ",
        returns_to_initial_state=False,
        abcd=("a)", "b)", "c)", "d)"),
        output_file_name=None,
    ):
        self.angular_correlation = angular_correlation
        self.delta_values = delta_values
        self.convention = convention
        self.theta_1 = theta_1
        self.theta_2 = theta_2
        self.returns_to_initial_state = returns_to_initial_state
        self.abcd = abcd
        self.output_file_name = output_file_name

        self.abs_delta_max = 100.0
        self.delta_ticks = np.arctan([-10.0, -1.5, -0.4, 0.0, 0.4, 1.5, 10.0])
        self.delta_tick_labels = ("-10.0", "-1.5", "-0.4", "0", "0.4", "1.5", "10.0")
        self.arctan_delta_lim = (-1.1 * 0.5 * np.pi, 1.1 * 0.5 * np.pi)
        self.arctan_delta_ticks = (
            -0.5 * np.pi,
            -0.25 * np.pi,
            0.0,
            0.25 * np.pi,
            0.5 * np.pi,
        )
        self.arctan_delta_tick_labels = (
            r"$-\pi/2$",
            r"$-\pi/4$",
            "0",
            r"$-\pi/4$",
            r"$-\pi/2$",
        )
        self.delta_label = r"\delta"
        self.level_scheme_delta_labels = []
        for delta in delta_values:
            if isinstance(delta, str):
                self.delta_label = delta
                self.level_scheme_delta_labels.append(r"$" + delta + r"$")
            else:
                self.level_scheme_delta_labels.append("")
        self.arctan_delta_label = r"\mathrm{arctan} (" + self.delta_label + r")"
        self.theta_1_label = r"\theta_1" if theta_1_label is None else theta_1_label
        self.ana_pow_1_label = r"A ( \theta = " + self.theta_1_label + r")"
        self.theta_2_label = r"\theta_2" if theta_2_label is None else theta_2_label
        self.ana_pow_2_label = r"A ( \theta = " + self.theta_2_label + r")"

        self.ana_pow_color = "black"
        self.abcd_position = (0.15, 0.9)
        self.abcd_fontsize = 14

    def evaluate(self, deltas):
        ana_pow_1 = np.zeros(len(deltas))
        ana_pow_2 = np.zeros(len(deltas))

        for i, delta in enumerate(deltas):
            initial_state = self.angular_correlation.initial_state
            cascade_steps = []
            for j, cas in enumerate(self.angular_correlation.cascade_steps):
                if isinstance(self.delta_values[j], str):
                    cascade_steps.append(
                        [
                            Transition(
                                cas[0].em_char,
                                cas[0].two_L,
                                cas[0].em_charp,
                                cas[0].two_Lp,
                                delta,
                            ),
                            cas[1],
                        ]
                    )
                else:
                    cascade_steps.append(
                        [
                            Transition(
                                cas[0].em_char,
                                cas[0].two_L,
                                cas[0].em_charp,
                                cas[0].two_Lp,
                                self.delta_values[j],
                            ),
                            cas[1],
                        ]
                    )
            ana_pow_1[i] = AnalyzingPower(
                AngularCorrelation(initial_state, cascade_steps), self.convention
            )(self.theta_1)
            ana_pow_2[i] = AnalyzingPower(
                AngularCorrelation(initial_state, cascade_steps), self.convention
            )(self.theta_2)

        return (ana_pow_1, ana_pow_2)

    def plot(self, n_delta=100):
        abs_delta_max = 100.0
        arctan_delta_max = np.arctan(abs_delta_max)
        arctan_delta = np.linspace(-arctan_delta_max, arctan_delta_max, n_delta)
        delta = np.tan(arctan_delta)
        ana_pow_1, ana_pow_2 = self.evaluate(delta)

        ana_pow_1_min = np.min(ana_pow_1)
        ana_pow_1_max = np.max(ana_pow_1)
        ana_pow_1_ran = ana_pow_1_max - ana_pow_1_min
        ana_pow_1_lim = (
            ana_pow_1_min - 0.1 * ana_pow_1_ran,
            ana_pow_1_max + 0.1 * ana_pow_1_ran,
        )

        ana_pow_2_min = np.min(ana_pow_2)
        ana_pow_2_max = np.max(ana_pow_2)
        ana_pow_2_ran = ana_pow_2_max - ana_pow_2_min
        ana_pow_2_lim = (
            ana_pow_2_min - 0.1 * ana_pow_2_ran,
            ana_pow_2_max + 0.1 * ana_pow_2_ran,
        )

        fig, ax = plt.subplots(2, 2, figsize=(7, 7))
        plt.subplots_adjust(wspace=0.1, hspace=0.1)

        ax[0][0].set_xlim(ana_pow_2_lim)
        ax[0][0].set_xticks([])
        ax[0][0].set_ylabel(r"$" + self.arctan_delta_label + r"$")
        ax[0][0].set_ylim(self.arctan_delta_lim)
        ax[0][0].set_yticks(self.arctan_delta_ticks)
        ax[0][0].set_yticklabels(self.arctan_delta_tick_labels)
        ax[0][0].plot(ana_pow_2, arctan_delta, color=self.ana_pow_color)
        ax_00x = ax[0][0].twiny()
        ax_00x.set_xlabel(r"$" + self.ana_pow_2_label + r"$")
        ax_00x.set_xlim(ana_pow_2_lim)
        ax_00y = ax[0][0].twinx()
        ax_00y.set_ylabel(r"$" + self.delta_label + r"$")
        ax_00y.set_ylim(self.arctan_delta_lim)
        ax_00y.set_yticks(self.delta_ticks)
        ax_00y.set_yticklabels(self.delta_tick_labels)
        if self.abcd is not None:
            ax[0][0].text(
                *self.abcd_position,
                self.abcd[0],
                horizontalalignment="center",
                verticalalignment="center",
                transform=ax[0][0].transAxes,
                fontsize=self.abcd_fontsize
            )

        ax[0][1].axis("off")
        level_scheme = LevelSchemePlotter(
            initial_state=self.angular_correlation.initial_state,
            cascade_steps=self.angular_correlation.cascade_steps,
            delta_labels=self.level_scheme_delta_labels,
            fontsize=10,
            returns_to_initial_state=self.returns_to_initial_state,
        )
        level_scheme.plot(ax[0][1])
        if self.abcd is not None:
            ax[0][1].text(
                *self.abcd_position,
                self.abcd[1],
                horizontalalignment="center",
                verticalalignment="center",
                transform=ax[0][1].transAxes,
                fontsize=self.abcd_fontsize
            )

        ax[1][0].set_xlabel(r"$" + self.ana_pow_2_label + r"$")
        ax[1][0].set_xlim(ana_pow_2_lim)
        ax[1][0].set_ylabel(r"$" + self.ana_pow_1_label + r"$")
        ax[1][0].set_ylim(ana_pow_1_lim)
        ax[1][0].plot(ana_pow_2, ana_pow_1, color=self.ana_pow_color)
        if self.abcd is not None:
            ax[1][0].text(
                *self.abcd_position,
                self.abcd[2],
                horizontalalignment="center",
                verticalalignment="center",
                transform=ax[1][0].transAxes,
                fontsize=self.abcd_fontsize
            )

        ax[1][1].set_xlabel(r"$" + self.arctan_delta_label + r"$")
        ax[1][1].set_xlim(self.arctan_delta_lim)
        ax[1][1].set_xticks(self.arctan_delta_ticks)
        ax[1][1].set_yticks([])
        ax_11x = ax[1][1].twiny()
        ax_11x.set_xlabel(r"$" + self.delta_label + r"$")
        ax_11x.set_xlim(self.arctan_delta_lim)
        ax_11x.set_xticks(self.delta_ticks)
        ax_11x.set_xticklabels(self.delta_tick_labels)
        ax_11y = ax[1][1].twinx()
        ax_11y.set_xticklabels(self.arctan_delta_tick_labels)
        ax_11y.set_ylabel(r"$" + self.ana_pow_1_label + r"$")
        ax_11y.set_ylim(ana_pow_1_lim)
        ax[1][1].plot(arctan_delta, ana_pow_1, color=self.ana_pow_color)
        if self.abcd is not None:
            ax[1][1].text(
                *self.abcd_position,
                self.abcd[3],
                horizontalalignment="center",
                verticalalignment="center",
                transform=ax[1][1].transAxes,
                fontsize=self.abcd_fontsize
            )

        if self.output_file_name:
            plt.savefig(self.output_file_name)