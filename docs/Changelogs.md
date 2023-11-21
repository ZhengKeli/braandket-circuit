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
