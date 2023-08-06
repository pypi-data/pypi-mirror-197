from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from attrs import define, field
from warpspeed.utils import J2
from warpspeed.steps import PromptStep, BaseToolStep
from warpspeed.artifacts import TextOutput, ErrorOutput

if TYPE_CHECKING:
    from warpspeed.artifacts import StructureArtifact


@define
class ToolSubstep(PromptStep):
    tool_step: BaseToolStep = field(kw_only=True)
    action_name: Optional[str] = field(default=None, kw_only=True)
    action_input: Optional[str] = field(default=None, kw_only=True)
    is_exiting: bool = field(default=False, kw_only=True)

    @property
    def parents(self) -> list[ToolSubstep]:
        return [self.tool_step.find_substep(parent_id) for parent_id in self.parent_ids]

    @property
    def children(self) -> list[ToolSubstep]:
        return [self.tool_step.find_substep(child_id) for child_id in self.child_ids]

    def before_run(self) -> None:
        self.structure.logger.info(f"Substep {self.id}\n{self.render_prompt()}")

    def run(self) -> StructureArtifact:
        try:
            if self.action_name == "exit":
                self.is_exiting = True
                self.output = TextOutput("ready for final output")
            elif self.action_name == "error":
                self.output = ErrorOutput(self.action_input, step=self)
            else:
                tool = self.tool_step.find_tool(self.action_name)

                if tool:
                    observation = tool.run(self.action_input)
                else:
                    observation = "tool not found"

                self.output = TextOutput(observation)
        except Exception as e:
            self.structure.logger.error(f"Substep {self.id}\nError: {type(e).__name__ }({e})")

            self.output = ErrorOutput(e, step=self)
        finally:
            return self.output

    def after_run(self) -> None:
        self.structure.logger.info(f"Substep {self.id}\nObservation: {self.output.value}")

    def render(self) -> str:
        return J2("prompts/steps/tool/substep.j2").render(
            step=self
        )

    def add_child(self, child: ToolSubstep) -> ToolSubstep:
        if child.id not in self.child_ids:
            self.child_ids.append(child.id)

        if self.id not in child.parent_ids:
            child.parent_ids.append(self.id)

        return child

    def add_parent(self, parent: ToolSubstep) -> ToolSubstep:
        if parent.id not in self.parent_ids:
            self.parent_ids.append(parent.id)

        if self.id not in parent.child_ids:
            parent.child_ids.append(self.id)

        return parent
