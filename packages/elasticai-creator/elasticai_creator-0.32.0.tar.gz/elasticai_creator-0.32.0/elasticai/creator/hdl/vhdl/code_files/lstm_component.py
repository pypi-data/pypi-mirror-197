from dataclasses import dataclass, field
from typing import Callable

from elasticai.creator.hdl.vhdl.code_files import (
    calculate_address_width,
    derive_fixed_point_params_from_factory,
)
from elasticai.creator.vhdl.number_representations import FixedPoint
from elasticai.creator.vhdl.templates import VHDLTemplate


@dataclass
class LSTMComponent:
    input_size: int
    hidden_size: int
    fixed_point_factory: Callable[[float], FixedPoint]
    layer_id: str
    work_library_name: str = field(default="work")

    def __post_init__(self) -> None:
        self.data_width, self.frac_width = derive_fixed_point_params_from_factory(
            self.fixed_point_factory
        )
        self.x_h_addr_width = calculate_address_width(
            self.input_size + self.hidden_size
        )
        self.hidden_addr_width = calculate_address_width(self.hidden_size)
        self.w_addr_width = calculate_address_width(
            (self.input_size + self.hidden_size) * self.hidden_size
        )

    @property
    def name(self) -> str:
        return f"lstm_{self.layer_id}.vhd"

    def lines(self) -> list[str]:
        template = VHDLTemplate(base_name="lstm")
        template.update_parameters(
            work_library_name=self.work_library_name,
            data_width=str(self.data_width),
            frac_width=str(self.frac_width),
            input_size=str(self.input_size),
            hidden_size=str(self.hidden_size),
            x_h_addr_width=str(self.x_h_addr_width),
            hidden_addr_width=str(self.hidden_addr_width),
            w_addr_width=str(self.w_addr_width),
            layer_name=self.layer_id,
        )
        return template.lines()
