# v0.2.4

New Features:

* Added trait `Conversion` together with `ToMatrix`
* Added `FlattenPass`

Improvements:

* Added examples about custom operations.

# v0.2.3

Breaking changes:

* Deleted trait `freeze`. Use `compile` with `FreezePass` instead.

New Features:

* Added new trait `compile` for circuit synthesis and optimization.
* Migrated all functionalities of `freeze` to `compile` using `FreezePass`.

Bug fixes:

* `apply()` now catch only `NotImplementedError`, raising other exceptions.

# v0.2.2

Breaking changes:

* Deleted package variable `__version__`.
* Changed the mechanism of the execution of `QOperation.__call__()`.
  The override method in subclasses is saved as `_custom_call` and executed by `default_impl`.
* Restricted the exposed API. Some unwanted APIs from subpackages are hidden.

New Features:

* Added `SymbolicRuntime` along with new trait `freeze`,
  which can parse custom operations into frozen ones (like `Sequential` and `RemappedByIndices`).

# v0.2.1

Breaking changes:

* Renamed `QParticle.n` to `QParticle.ndim`.
* Changed the mechanism of `QOperation.__call__()`. Now it is automatically registered as "apply impls".
* Changed the mechanism of `allocate_particle()`. Now it is a call of operation `AllocateParticle`.
* Moved definitions of `QRuntime` and `apply()` to subpackage `traits.runtime`.
  And split the implementation part from subpackage `traits` to `traits_impls`.

Bug fixes:

* Fixed the bug in `apply()` which occurs when `len(impls_error)==1`.
* Fixed a bug in `resolve_type_and_instance()`,
  which occurs when `type_or_instance is None` but `base_type is not None`.

Improvements:

* updated the examples.
