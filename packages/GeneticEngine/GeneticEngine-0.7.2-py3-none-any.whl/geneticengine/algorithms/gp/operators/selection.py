from __future__ import annotations

import numpy as np

from geneticengine.algorithms.gp.individual import Individual
from geneticengine.algorithms.gp.structure import GeneticStep
from geneticengine.core.problems import FitnessMultiObjective, MultiObjectiveProblem
from geneticengine.core.problems import Problem
from geneticengine.core.problems import SingleObjectiveProblem
from geneticengine.core.random.sources import Source
from geneticengine.core.representations.api import Representation
from geneticengine.core.evaluators import Evaluator


class TournamentSelection(GeneticStep):
    """TournamentSelection represents a tournament selection algorithm, where
    tournament_size individuals are selected at random, and only the best
    passes to the next generation."""

    def __init__(self, tournament_size: int, with_replacement: bool = False):
        """
        Args:
            tournament_size (int): number of individuals from the population that will be randomly selected
        """
        self.tournament_size = tournament_size
        self.with_replacement = with_replacement

    def iterate(
        self,
        problem: Problem,
        evaluator: Evaluator,
        representation: Representation,
        r: Source,
        population: list[Individual],
        target_size: int,
        generation: int,
    ) -> list[Individual]:
        assert isinstance(problem, SingleObjectiveProblem)
        winners: list[Individual] = []
        candidates = population.copy()
        evaluator.eval(problem, candidates)
        for _ in range(target_size):
            candidates = [r.choice(population) for _ in range(self.tournament_size)]
            winner = max(candidates, key=Individual.key_function(problem))
            winners.append(winner)

            if self.with_replacement:
                candidates.remove(winner)
                if not candidates:
                    candidates = population.copy()
        assert len(winners) == target_size
        return winners


class LexicaseSelection(GeneticStep):
    """Implements Lexicase Selection
    (http://williamlacava.com/research/lexicase/)."""

    def __init__(self, epsilon: bool = False):
        """
        Args:
            epsilon: if True, espilon-lexicase is performed. We use the method given by equation 5 in
                https://dl.acm.org/doi/pdf/10.1145/2908812.2908898.
        """
        self.epsilon = epsilon

    def iterate(
        self,
        problem: Problem,
        evaluator: Evaluator,
        representation: Representation,
        r: Source,
        population: list[Individual],
        target_size: int,
        generation: int,
    ) -> list[Individual]:
        assert isinstance(problem, MultiObjectiveProblem)
        candidates = population.copy()
        evaluator.eval(problem, candidates)
        n_cases = problem.number_of_objectives()
        cases = r.shuffle(list(range(n_cases)))
        winners = []

        for _ in range(target_size):
            candidates_to_check = candidates.copy()

            while len(candidates_to_check) > 1 and cases:
                new_candidates: list[Individual] = list()
                c = cases.pop(0)

                choose_best = min if problem.minimize[c] else max

                best_fitness = choose_best([x.fitness[c] for x in candidates_to_check])  # type: ignore
                checking_value = best_fitness

                if self.epsilon:

                    def get_fitness_value(ind: Individual, c: int):
                        fitnesses = ind.get_fitness(problem)
                        assert isinstance(fitnesses, FitnessMultiObjective)
                        return fitnesses.multiple_fitnesses[c]

                    fitness_values = np.array(
                        [get_fitness_value(x, c) for x in candidates_to_check if not np.isnan(get_fitness_value(x, c))],
                    )
                    mad = np.median(np.absolute(fitness_values - np.median(fitness_values)))
                    checking_value = best_fitness + mad if problem.minimize[c] else best_fitness - mad

                for checking_candidate in candidates_to_check:
                    fitnesses = checking_candidate.get_fitness(problem)
                    assert isinstance(fitnesses, FitnessMultiObjective)
                    if problem.minimize[c]:
                        add_candidate = fitnesses.multiple_fitnesses[c] <= checking_value
                    else:
                        add_candidate = fitnesses.multiple_fitnesses[c] >= checking_value
                    if add_candidate:
                        new_candidates.append(checking_candidate)

                candidates_to_check = new_candidates.copy()

            winner = r.choice(candidates_to_check) if len(candidates_to_check) > 1 else candidates_to_check[0]
            assert isinstance(winner.get_fitness(problem), list)
            winners.append(winner)
            candidates.remove(winner)
        return winners
