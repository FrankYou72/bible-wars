from ..models.consequence import Consequence
from ...utils.exceptions import IncorrectInstance


def apply_consequence(consequence, object):
    if object.__class__.__name__ != consequence.instance:
        raise IncorrectInstance

    command = f"object.{consequence.attribute} = object.{consequence.attribute} {consequence.operation} {consequence.factor}"
    exec(command)
