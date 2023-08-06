lib: nixpkgs: python_version: let
  utils = import ./override_utils.nix;
  pkgs_overrides = override: python_pkgs: builtins.mapAttrs (_: override python_pkgs) python_pkgs;

  layer_1 = python_pkgs:
    python_pkgs
    // {
      import-linter = import ./import-linter.nix lib python_pkgs;
      more-itertools = import ./more-itertools.nix lib python_pkgs;
      types-deprecated = import ./deprecated/stubs.nix lib;
      types-simplejson = import ./simplejson/stubs.nix lib;
    };

  pluggy_override = python_pkgs: utils.replace_pkg ["pluggy"] (python_pkgs.pluggy);
  networkx_override = python_pkgs: utils.replace_pkg ["networkx"] (import ./networkx.nix lib python_pkgs);
  overrides = map pkgs_overrides [
    pluggy_override
    networkx_override
  ];

  final_nixpkgs = utils.compose ([layer_1] ++ overrides) nixpkgs."${python_version}Packages";
in
  final_nixpkgs
