import os
import warnings
from copy import deepcopy

import numpy as np
import pandas as pd
import yaml
from hdmf.common import DynamicTable
from hdmf.utils import docval, get_docval, popargs, popargs_to_dict

from pynwb import get_class, load_namespaces, register_class

from .utils import is_na_or_empty, request_pubchem

ALLOW_ACCOMPANNIED_DTYPES = {"str": str, "int": int}
NOT_AVAILABLE_DEFAULT = "N/A"

namespace_name = "ndx-odor-metadata"
namespace_path = os.path.join("spec", namespace_name + ".namespace.yaml")
extension_path = os.path.join("spec", namespace_name + ".extensions.yaml")
initfile_path = os.path.dirname(__file__)

# Set path of the namespace/extension.yaml file to the expected install location
# If the extension has not been installed yet but we are running directly from
# the git repo

namespace_path = os.path.join(initfile_path, namespace_path)
if not os.path.exists(namespace_path):
    namespace_path = os.path.abspath(
        os.path.join(initfile_path, "..", "..", "..", namespace_path)
    )

extension_path = os.path.join(initfile_path, extension_path)
if not os.path.exists(extension_path):
    extension_path = os.path.abspath(
        os.path.join(initfile_path, "..", "..", "..", extension_path)
    )


# Load the namespace
load_namespaces(namespace_path)

# Import for accessibility at the package level
OdorMetaData = get_class("OdorMetaData", "ndx-odor-metadata")


# Prepare for modifying API
def __prepare_classdef__(ext_grp, col_meta_constr):
    rm_vars = ["required", "index", "class"]

    dtype_map = {
        "float": float,
        "float32": float,
        "double": np.float64,
        "float64": np.float64,
        "long": np.int64,
        "int64": np.int64,
        "int": int,
        "int32": int,
        "short": np.int16,
        "int16": np.int16,
        "int8": np.int8,
        "uint": np.uint32,
        "uint64": np.uint64,
        "uint32": np.uint32,
        "uint16": np.uint16,
        "uint8": np.uint8,
        "bool": bool,
        "text": str,
    }

    init_attrs = ext_grp["attributes"]

    for d_attr in init_attrs:
        for k in rm_vars:
            d_attr.pop(k, None)

        assert (
            _dtype_str := d_attr.pop("dtype", None)
        ) is not None, f"Missing 'dtype' for field '{k}' of `OdorMetaData.attributes` in extension file"
        assert (
            _dtype := dtype_map.get(_dtype_str, None)
        ) is not None, f"The `dtype='{_dtype_str}' for field '{k}' of `OdorMetaData.attributes` in extension file"
        d_attr["type"] = _dtype

        if "default_value" in d_attr:
            d_attr["default"] = d_attr.pop("default_value")

    col_meta_from_file = ext_grp["datasets"]
    col_meta_from_file = {x.pop("name"): x for x in col_meta_from_file}

    col_meta_from_load = {x.pop("name"): x for x in list(deepcopy(col_meta_constr))}

    _loadkeys = set(col_meta_from_load.keys())
    _filekeys = set([k for k in col_meta_from_file.keys() if not k.endswith("_index")])

    assert len(_key_diff := _loadkeys.symmetric_difference(_filekeys)) == 0, (
        "Mismatch of key sets between loaded `OdorMetaData.__columns__`"
        f"and from extension file:\n {list(_key_diff)}"
    )

    addfn_docval = []
    indexable_dtypes = dict()

    file_cols = col_meta_from_file.keys()
    cols_with_dtype = {
        k: k_dtype for k in file_cols if (k_dtype := k + "_dtype") in file_cols
    }
    cols_with_def_na = []

    for k, d_file in col_meta_from_file.items():
        if k.endswith("_index"):
            continue
        d_load = col_meta_from_load[k]
        d_load["doc"] = d_load.pop("description", "[Missing doc]")
        if (
            "type" not in d_load
            and type(_dtype_str := d_file.get("dtype", None)) is str
        ):
            assert (
                _dtype := dtype_map.get(_dtype_str, None)
            ) is not None, (
                f"The `dtype='{_dtype_str}' for '{k}' is not allowed at this point"
            )

            d_load["type"] = _dtype
            if d_load.get("index", False):
                d_load["type"] = (_dtype, list, tuple)
                indexable_dtypes[k] = _dtype

        for rm_k in rm_vars:
            d_load.pop(rm_k, None)

        defval_is_NA = False
        if "default_value" in d_file:
            assert "default" not in d_load, (
                f'The key "default" is not supposed to be in the "{k}"'
                "of the loaded `OdorMetaData.__columns__`"
            )
            def_val = d_file["default_value"]
            d_load["default"] = def_val
            if isinstance(def_val, str):
                defval_is_NA = def_val.upper() == NOT_AVAILABLE_DEFAULT.upper()

        # so don't handle list-able columns
        defval_is_NA = defval_is_NA and k not in indexable_dtypes
        if defval_is_NA:
            cols_with_def_na.append(k)

        has_dtype_col = k in cols_with_dtype
        if has_dtype_col or defval_is_NA:
            _dtype_def = d_load.get("type", None)

            if has_dtype_col:
                allow_dtypes = list(ALLOW_ACCOMPANNIED_DTYPES.values())
            else:
                allow_dtypes = [
                    float
                ]  # this is to handle np.nan when using pd.read_[X]

            if _dtype_def is None:
                d_load["type"] = tuple(allow_dtypes)
            else:
                if type(_dtype_def) not in [list, tuple, set]:
                    _dtype_def = list([_dtype_def])
                d_load["type"] = tuple(set(_dtype_def + allow_dtypes))

        addfn_docval.append(dict(name=k, **d_load))

    return init_attrs, addfn_docval, indexable_dtypes, cols_with_dtype, cols_with_def_na


col_meta_constr = deepcopy(OdorMetaData.__columns__)

with open(extension_path, "r") as f:
    _ext_data = yaml.safe_load(f)

ext_grp = pd.DataFrame(_ext_data["groups"]).query(
    'neurodata_type_def == "OdorMetaData"'
)
assert len(ext_grp) == 1, "There should only be 1 `OdorMetaData` object"
ext_grp = ext_grp.iloc[0].to_dict()

(
    init_attrs,
    addfn_docval,
    indexable_dtypes,
    cols_with_dtype,
    cols_with_def_na,
) = __prepare_classdef__(ext_grp, col_meta_constr)


# Create custom API
@register_class("OdorMetaData", namespace_name)
class OdorMetaData(DynamicTable):
    __nwbfields__ = ("name", "description")
    __defaultname__ = "odor_table"
    __columns__ = col_meta_constr

    __special_delimiters__ = {"__default_delimiter__": ",", "chemical_synonyms": "\n"}

    @docval(
        {
            "name": "name",
            "type": str,
            "doc": "name of this OdorMetaData table",
            "default": ext_grp["default_name"],
        },
        *init_attrs,
        *get_docval(OdorMetaData.__init__, "id", "columns", "colnames"),
    )
    def __init__(self, **kwargs):
        pop_out_ls = ["name", "description", "id", "columns", "colnames"]
        dyntbl_kwargs = popargs_to_dict(pop_out_ls, kwargs)
        super().__init__(**dyntbl_kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __process_column_with_accompanied_dtype__(self, rkwargs, val_col, dtype_col):
        val = rkwargs.get(val_col, None)
        infered_dtype = type(val).__name__
        dtype = rkwargs.get(dtype_col, None)
        if is_na_or_empty(dtype):
            dtype = infered_dtype

        assert val is not None, f"Currently do not support `{val_col}=None`"
        assert dtype == infered_dtype, (
            f"Mismatch dtype `{dtype_col}` "
            f'from provided ("{dtype}") and inferred ("{infered_dtype}")'
        )
        assert (
            dtype in ALLOW_ACCOMPANNIED_DTYPES
        ), f"Only support {ALLOW_ACCOMPANNIED_DTYPES} for `{dtype_col}`"

        rkwargs[val_col] = str(val)
        rkwargs[dtype_col] = dtype
        return rkwargs

    def __check_valid_main_columns__(self, rkwargs):
        # TODO: put these in class attributes
        non_dup_keys = ["raw_id"]
        non_nan_keys = ["raw_id", "stim_id", "stim_name", "stim_types"]

        for nn_k in non_nan_keys:
            val_nn = rkwargs.get(nn_k, None)
            assert not is_na_or_empty(
                val_nn
            ), f"Column/key `{nn_k}` is missing, invalid or N/A."

        for nd_k in non_dup_keys:
            val_nd = rkwargs.get(nd_k, None)
            assert val_nd is not None, f"Missing column/key `{nd_k}`"
            assert val_nd not in self.get(nd_k), (
                f"Potential duplicates found at `{nd_k}`. "
                f"`{nd_k}={val_nd}` already exists."
            )

    def __precheck_chemical_columns__(self, rkwargs, accept_plurals=True):
        # TODO: add to class attr
        # TODO: limit `types_with_pubchem` with only singular?
        types_with_pubchem = {"odor", "odour", "chem", "chemical", "chm"}

        if accept_plurals:
            types_with_pubchem.union({"odors", "odours", "chemicals"})

        odor_non_nan_keys = [
            "pubchem_id",
            "chemical_dilution_type",
            "chemical_concentration",
            "chemical_concentration_unit",
            "chemical_provider",
        ]

        # first check `pubchem_id`
        pubchem_id = rkwargs.get("pubchem_id", np.nan)
        has_pubchem = not np.isnan(pubchem_id)

        # then check whether `stim_types` contains chemical-like tags
        rkwargs = self.__process_indexable_column__(
            rkwargs, col="stim_types", dtype=indexable_dtypes["stim_types"]
        )

        stim_types = {x.lower() for x in rkwargs.get("stim_types", [])}
        has_odor = len(stim_types.intersection(types_with_pubchem)) > 0

        # these 2 have to agree
        assert has_pubchem == has_odor, (
            f"Either (1) `pubchem_id` ({pubchem_id}) has to be non-nan "
            f"and `stim_types` ({stim_types}) contains {types_with_pubchem}. "
            f"Or (2) `pubchem_id` ({pubchem_id}) is not provided "
            f"and `stim_types` ({stim_types}) does NOT contain {types_with_pubchem}."
        )

        pubchem_queryable = has_pubchem and has_odor

        # If queryable, double chemical columns to make sure they are filled
        query_ready = False
        if pubchem_queryable:
            for onn_k in odor_non_nan_keys:
                val_onn = rkwargs.get(onn_k, None)
                assert not is_na_or_empty(val_onn), (
                    f"Column/key `{onn_k}` is missing, invalid or N/A. "
                    "This is not acceptable when `pubchem_id` is provided, "
                    "and `stim_types` indicates presence of odor"
                )
            query_ready = True

        pubchem_ready = pubchem_queryable and query_ready
        return rkwargs, pubchem_ready, pubchem_id

    def __process_pubchem_queries__(self, rkwargs, query_results, overwrite=True):
        suppress_warn_keys = ["is_validated"]
        _ovw_str = "Will overwrite" if overwrite else "Will NOT overwrite"
        for ch_k, ch_v in query_results.items():
            arg_v = rkwargs.get(ch_k, None)
            arg_v_is_empty = is_na_or_empty(arg_v)

            if arg_v_is_empty:
                rkwargs[ch_k] = ch_v
                continue

            # if not empty/NA
            if ch_k not in suppress_warn_keys:
                warnings.warn(
                    f"The given argument `{ch_k}` is not empty or N/A or NaN. "
                    f"{_ovw_str} this argument. "
                    "Change `overwrite_pubchem_queries` if not desired."
                )

            if overwrite:
                rkwargs[ch_k] = ch_v
        return rkwargs

    def __process_indexable_column__(self, rkwargs, col, dtype):
        default_delim = self.__special_delimiters__["__default_delimiter__"]
        val = rkwargs.get(col, None)
        if dtype is str and isinstance(val, str):
            delim = self.__special_delimiters__.get(col, default_delim)
            rkwargs[col] = [s.strip() for s in val.split(delim) if not s.isspace()]
        return rkwargs

    @docval(
        *addfn_docval,
        {
            "name": "accept_plural_chemtype",
            "type": bool,
            "default": True,
            "doc": "Whether to accept plurals when considering if `stim_type` indicates odor/chemical",
        },
        {
            "name": "query_pubchem",
            "type": bool,
            "default": True,
            "doc": "Whether to use PubChemPy to query at all.",
        },
        {
            "name": "return_synonyms",
            "type": bool,
            "default": True,
            "doc": "Whether to save synonyms also.",
        },
        {
            "name": "warn_notfound_synonym",
            "type": bool,
            "default": True,
            "doc": "Whether to warn if the given `stim_name` cannot be found in queried synonyms.",
        },
        {
            "name": "error_notfound_cid",
            "type": bool,
            "default": True,
            "doc": "Whether to throw an error when given `pubchem_id` cannot be found on PubChem CID",
        },
        {
            "name": "overwrite_pubchem_queries",
            "type": bool,
            "default": True,
            "doc": "Whether to overwrite the given arguments about information that "
            "could conflict with the metadata queried from PubChem using PubChemPy. "
            "Only applicable if `query_pubchem = True`",
        },
        allow_extra=True,
    )
    def add_stimulus(self, **kwargs):
        accept_plural_chemtype = popargs("accept_plural_chemtype", kwargs)
        pcp_request_opts = popargs_to_dict(
            ["return_synonyms", "warn_notfound_synonym", "error_notfound_cid"], kwargs
        )
        pcp_query_opts = popargs_to_dict(
            ["query_pubchem", "overwrite_pubchem_queries"], kwargs
        )

        rkwargs = dict(kwargs)

        # Process IDs first, copy `raw_id` over if `stim_id` is not provided
        raw_id_val = rkwargs.get("raw_id", None)
        assert raw_id_val is not None, "Need a valid `raw_id` input"
        rkwargs["stim_id"] = rkwargs.get("stim_id", raw_id_val)

        # Process columns with accompanying dtype-columns
        for val_col, dtype_col in cols_with_dtype.items():
            rkwargs = self.__process_column_with_accompanied_dtype__(
                rkwargs, val_col, dtype_col
            )

        # Check for non-duplicates and non-(nan/empty) for main columns
        self.__check_valid_main_columns__(rkwargs)

        # Pre-check chemical columns
        rkwargs, pubchem_ready, pubchem_id = self.__precheck_chemical_columns__(
            rkwargs, accept_plurals=accept_plural_chemtype
        )

        # Query PubChem
        chem_meta = dict()
        if pubchem_ready and pcp_query_opts["query_pubchem"]:
            chem_meta = request_pubchem(
                cid=int(pubchem_id),
                name=rkwargs.get("stim_name", ""),
                synonym_delim=self.__special_delimiters__["chemical_synonyms"],
                **pcp_request_opts,
            )

        # Save/overwrite PubChem queried data
        rkwargs = self.__process_pubchem_queries__(
            rkwargs,
            query_results=chem_meta,
            overwrite=pcp_query_opts["overwrite_pubchem_queries"],
        )

        # Process list-able columns
        for col, dtype in indexable_dtypes.items():
            rkwargs = self.__process_indexable_column__(rkwargs, col, dtype)

        # Back-fill N/A values if not list-able column
        for col in cols_with_def_na:
            val = rkwargs.get(col, None)
            if is_na_or_empty(val):
                rkwargs[col] = NOT_AVAILABLE_DEFAULT

        return super().add_row(**rkwargs)
