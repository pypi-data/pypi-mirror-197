from sklearn import metrics

from proteinshake.datasets import ProteinLigandInterfaceDataset
from proteinshake.tasks import Task

class LigandAffinityTask(Task):
    """ Predict the dissociation constant (kd) for a protein and a small molecule. This is a protein-level regression task.
    Small molecule ligand information is stored as ``dataset[i].smiles`` for a SMILES string, or as pre-computed molecular
    fingerprints ``dataset[i].fp_maccs``, ```dataset[i].fp_morgan_r2``.
    """
    
    DatasetClass = ProteinLigandInterfaceDataset

    @property
    def task_type(self):
        return "regression"

    def target(self, protein):
        return protein['protein']['neglog_aff']

    def evaluate(self, y_pred):
        return {
            'mse': metrics.mean_squared_error(self.test_targets, y_pred),
            'r2': metrics.r2_score(self.test_targets, y_pred)
        }
