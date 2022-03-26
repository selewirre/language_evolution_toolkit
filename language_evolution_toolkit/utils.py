from multipledispatch import dispatch
from typing import Dict, Any
from uuid import uuid4, UUID


class ImmutableProperty:
    """
    ImmutableProperty is a descriptor for class properties that can not be set by the user.
    """
    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        return instance.__dict__['_' + self._name]


class TrackingID:
    """
    TrackingID is a class that holds information that will help track LinguisticObjects throughout multiple steps of
    language evolution.

    Attributes
    ----------
    root: UUID
        A unique identification instance/number. It represents the core of an object's evolution tree.
    branch: str
        A string separating each generation with a '.'. For example, a branch = '1.2.5.1.23' means that there has been
        a total of 5 generations, and our specific leaf belongs to the 23rd branch of the 1st branch of the 5th branch
        of the 2nd branch of the 1st branch of the root.
    leaf: int
        An integer that indicates the numbered variance of the a specific branch. In the next evolutionary step, the
        leaf will become the newest branch (appended at the end of the branch string).
    generations: int
        An integer that depicts the generation number of the TrackingID

    Example
    -------
    >>> a = TrackingID()
    >>> b = TrackingID.from_parent_branch(a)
    >>> c = TrackingID.from_parent_branch(b)

    """

    root: UUID = ImmutableProperty()
    branch: str = ImmutableProperty()
    leaf: int = ImmutableProperty()
    generations: int = ImmutableProperty()

    @dispatch()
    def __init__(self):
        self._root: UUID = uuid4()
        self._branch: str = ''
        self._leaf: int = 1
        self.__post_init__()

    @dispatch(UUID)
    def __init__(self, root: UUID):
        self._root: UUID = root
        self._branch: str = ''
        self._leaf: int = 1
        self.__post_init__()

    @dispatch(UUID, str)
    def __init__(self, root: UUID, branch: str):
        self._root: UUID = root
        self._branch: str = branch
        self._leaf: int = 1
        self.__post_init__()

    @dispatch(UUID, str, int)
    def __init__(self, root: UUID, branch: str, leaf: int):
        self._root: UUID = root
        self._branch: str = branch
        self._leaf: int = leaf
        self.__post_init__()

    def __post_init__(self):
        self._set_generations()

    def _set_generations(self):
        self._generations: int = len(self.branch.split('.')) + 1

    @classmethod
    def from_parent_branch(cls, parent_tracking_id: "TrackingID", new_leaf: int = 1) -> "TrackingID":
        """
        Defining a new TrackingID by providing the parent branch and the new leaf number.

        Parameters
        ----------
        parent_tracking_id: TrackingID
            The parent.
        new_leaf:
            The new lead number.

        Returns
        -------
        TrackingID
        """
        if parent_tracking_id.branch:
            new_branch = f'{parent_tracking_id.branch}.{parent_tracking_id.leaf}'
        else:
            new_branch = f'{parent_tracking_id.leaf}'

        return cls(parent_tracking_id.root, new_branch, new_leaf)

    def __hash__(self) -> int:
        return hash((self.root, self.branch, self.leaf))

    def __eq__(self, other: "TrackingID") -> bool:
        """
        Parameters
        ----------
        other: TrackingID
            The object we are comparing to.

        Returns
        -------
        bool
            False if the class is not the same, True if all values of interest are the same, False otherwise.
        """

        if not self.__class__.__name__ == other.__class__.__name__:
            return False
        else:
            self_values = (self.root, self.branch, self.leaf)
            other_values = (other.root, other.branch, other.leaf)
            return self_values == other_values

    def __repr__(self) -> str:
        """
        Returns
        -------
        str
            The keys and values of all the properties (root, branch, and leaf), alongside the class name.
        """

        repr_list = [f'{key}={value!r}'
                     for key, value in {'root': self.root, 'branch': self.branch, 'leaf': self.leaf}.items()]
        repr_string = ', '.join(repr_list)
        repr_string = f"{self.__class__.__name__}({repr_string})"
        return repr_string


class LinguisticObject:
    """
    LinguisticObject is a generic object that contains ImmutableProperties. These ImmutableProperties are the defining
    characteristics of the object. The object is compared (__eq__), represented (__repr__) and hashed (__hash__) based
    on them.

    Attributes
    ----------
    __immutables_dict__: Dict[str, Any]
        A dictionary that holds all the attributes of the class that are of type "ImmutableProperty".
    tracking_id: TrackingID
        A variable to assist in tracking down the LinguisticObject throughout multiple evolutionary steps of a language.
    """

    tracking_id: TrackingID = ImmutableProperty()

    def __init__(self, tracking_id: TrackingID = None):
        self._set_tracking_id(tracking_id)
        self.__immutables_dict__: Dict[str, Any] = {key: self.__getattribute__(key)
                                                    for key, value in self.__class__.__dict__.items()
                                                    if isinstance(value, ImmutableProperty)
                                                    and key not in ['tracking_id']}

    def _set_tracking_id(self, tracking_id):
        if tracking_id:
            self._tracking_id = tracking_id
        else:
            self._tracking_id = TrackingID()

    def __hash__(self) -> int:
        return hash(self.__immutables_dict__.values())

    def __eq__(self, other: "LinguisticObject") -> bool:
        """
        Parameters
        ----------
        other: LinguisticObject
            The object we are comparing to.

        Returns
        -------
        bool
            False if the class is not the same, True if all immutable properties' values are the same, False otherwise.
        """

        if not self.__class__.__name__ == other.__class__.__name__:
            return False
        else:
            self_values = tuple(self.__immutables_dict__.values())
            other_values = tuple(other.__immutables_dict__.values())
            return self_values == other_values

    def __repr__(self) -> str:
        """
        Returns
        -------
        str
            The keys and values of all the immutable properties, alongside the class name.
        """

        repr_list = [f'{key}={value!r}' for key, value in self.__immutables_dict__.items()]
        repr_string = ', '.join(repr_list)
        repr_string = f"{self.__class__.__name__}({repr_string})"
        return repr_string
