class Trial:
    """Trial class
    - Initialized when an experiment is submitted
    - Creates and manages experiment directory
    - Has access to the AFPO-level pickle file
    """
    def __init__(self, run_idx, experiment_directory, experiment_parameters):
        self.run_idx = run_idx
        self.experiment_directory = experiment_directory
        self.trial_directory = self.experiment_directory + f'/trial_{run_idx}'
        self.pickle_file = f'{self.trial_directory}/trial_{run_idx}.pkl'

        self.afpo = AgeFitnessPareto(experiment_parameters, run_id=run_idx, dir=f'{self.experiment_directory}/trial_{run_idx}')
        self.max_generations = experiment_parameters['generations']
        self.current_generation = 0
        # Create trial pickle file for Trial object (self)
        with open(self.pickle_file, 'wb') as pickle_file:
            pickle.dump(self, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)

    def Run(self):
        """Run the different runs until we max out"""
        while self.current_generation < self.max_generations:
            self.Run_One_Generation()

    def Run_One_Generation(self):
        """Run a single generation of the trial"""
        t_start = time.time()

        # 1. Save population pickle file (for insurance)
        os.system(f'cp {self.pickle_file} {self.trial_directory}/saved_trial_{self.run_idx}.pkl')
        
        # 2. Compute a single generation for this trial
        print(f'\n\n========== \n Generation {self.afpo.currentGen} - Run {self.afpo.run_id} \n ==========\n\n')
        self.afpo.Evolve_One_Generation()
        # self.afpo.Clean_Directory()

        # 3. Update pickle file
        with open(self.pickle_file, 'wb') as pickle_file:
            pickle.dump(self, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)

        self.current_generation += 1

        t_end = time.time()
        self.one_gen_time = t_end - t_start