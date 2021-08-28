"""
Copyright 2019 Marco Lattuada

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import copy

import model_building.design_space
import model_building.hyperopt_sfs_experiment_configuration


class SFSExpConfsGenerator(model_building.design_space.ExpConfsGenerator):
    """
    Generator for using SFS selection

    The class wraps an ExpConfsGenerator to apply SFS for performing feature selection on the input dataset; the SFS is used to filter the columns of the dataset which is passed as argument to the wrapped generator

    Attributes
    ----------
    wrapped_generator: ExpConfsGenerator
        The ExpConfsGenerator used with the feature selector

    Methods
    ------
    generate_experiment_configurations()
        Generates the set of expriment configurations to be evaluated
    """

    def __init__(self, wrapped_generator, campaign_configuration, seed):
        """
        Parameters
        ----------
        wrapped_generator: ExpConfsGenerator
            The ExpConfsGenerator to be used coupled with the current feature selector

        campaign_configuration: dict of str: dict of str: str
            The set of options specified by the user though command line and campaign configuration files

        seed: integer
            The seed to be used in random based activities
        """
        super().__init__(campaign_configuration, seed)
        self._wrapped_generator = wrapped_generator

    def generate_experiment_configurations(self, prefix, regression_inputs):
        """
        Generates the set of experiment configurations to be evaluated

        Parameters
        ----------
        prefix: list of str
            The prefix to be used for the signature of the ExperimentConfiguration generated by this generator

        regression_inputs: RegressionInputs
            The data to be used by the ExperimentConfiguration

        Returns
        -------
        list of ExperimentConfiguration
            a list of the experiment configurations to be evaluated
        """
        self._logger.info("-->Generating experiments by SFSExpConfsGenerator")
        internal_list = self._wrapped_generator.generate_experiment_configurations(prefix, regression_inputs)
        ret_list = []
        for wrapped_point in internal_list:
            ret_list.append(model_building.hyperopt_sfs_experiment_configuration.SFSExperimentConfiguration(self._campaign_configuration, copy.deepcopy(regression_inputs), prefix, wrapped_point))
        self._logger.info("<--")
        return ret_list

    def __deepcopy__(self, memo):
        return SFSExpConfsGenerator(copy.deepcopy(self._wrapped_generator), self._campaign_configuration, self._random_generator.random())



class HyperoptExpConfsGenerator(model_building.design_space.ExpConfsGenerator):
    def __init__(self, wrapped_generator, campaign_configuration, seed):
        super().__init__(campaign_configuration, seed)
        self._wrapped_generator = wrapped_generator

    def generate_experiment_configurations(self, prefix, regression_inputs):
        self._logger.info("-->Generating experiments by HyperoptExpConfsGenerator")
        internal_list = self._wrapped_generator.generate_experiment_configurations(prefix, regression_inputs)
        ret_list = []
        for wrapped_point in internal_list:
            ret_list.append(model_building.hyperopt_sfs_experiment_configuration.HyperoptExperimentConfiguration(self._campaign_configuration, copy.deepcopy(regression_inputs), prefix, wrapped_point))
        self._logger.info("<--")
        return ret_list

    def __deepcopy__(self, memo):
        return HyperoptExpConfsGenerator(copy.deepcopy(self._wrapped_generator), self._campaign_configuration, self._random_generator.random())



class HyperoptSFSExpConfsGenerator(model_building.design_space.ExpConfsGenerator):
    def __init__(self, wrapped_generator, campaign_configuration, seed):
        super().__init__(campaign_configuration, seed)
        self._wrapped_generator = wrapped_generator

    def generate_experiment_configurations(self, prefix, regression_inputs):
        self._logger.info("-->Generating experiments by HyperoptSFSExpConfsGenerator")
        internal_list = self._wrapped_generator.generate_experiment_configurations(prefix, regression_inputs)
        ret_list = []
        for wrapped_point in internal_list:
            ret_list.append(model_building.hyperopt_sfs_experiment_configuration.HyperoptSFSExperimentConfiguration(self._campaign_configuration, copy.deepcopy(regression_inputs), prefix, wrapped_point))
        self._logger.info("<--")
        return ret_list

    def __deepcopy__(self, memo):
        return HyperoptSFSExpConfsGenerator(copy.deepcopy(self._wrapped_generator), self._campaign_configuration, self._random_generator.random())
