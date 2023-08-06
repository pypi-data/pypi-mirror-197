from judo.data_types import dtype

from fragile.core.api_classes import Callback
from fragile.core.typing import StateDict


class StoreInitAction(Callback):
    name = "store_init_action"
    default_inputs = {"init_actions": {"clone": True}}
    default_outputs = ("init_actions",)

    @property
    def param_dict(self) -> StateDict:
        return {"init_actions": dict(self.swarm.param_dict["actions"])}

    def before_env(self):
        if self.swarm.epoch == 0:
            self.update(init_actions=self.get("actions").copy())


class TrackWalkersId(Callback):
    default_inputs = {"id_walkers": {"clone": True}, "parent_ids": {"clone": True}}
    default_param_dict = {
        "id_walkers": {"dtype": dtype.hash_type},
        "parent_ids": {"dtype": dtype.hash_type},
    }

    def update_ids(self, inactives: bool = True):
        name = "states" if "states" in self.swarm.state.names else "observs"
        new_ids_all = self.swarm.state.hash_batch(name)
        parent_ids = self.get("parent_ids", inactives=inactives).copy()
        new_ids = self.get("id_walkers", inactives=True).copy()
        parent_ids[self.swarm.state.actives] = new_ids[self.swarm.state.actives].copy()
        new_ids[self.swarm.state.actives] = new_ids_all[self.swarm.state.actives]
        self.update(
            parent_ids=parent_ids,
            id_walkers=new_ids,
            inactives=inactives,
        )

    def after_env(self):
        self.update_ids()
