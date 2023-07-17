import traceback
from src.main.protobuf import analysis_v2_pb2

option_srcs = "srcs"
option_hdrs = "hdrs"
option_copts = "copts"
option_linkopts = "linkopts"

value_catalog = "-lcatalog"
value_nostdinc = "-nostdinc"
value_nostdlib = "-nostdlib"

value_nostd_inc_cplus = "-nostdinc++"
value_nostdlib_cplus = "-nostdlib++"

value_std_cplus_11 = "-std=c++11"
value_std_cplus_14 = "-std=c++14"
value_std_cplus_17 = "-std=c++17"
value_qnx_source = "-D_QNX_SOURCE"

value_libm = "-lm"
value_fno_builtin = "-fno-builtin"

value_y_gpp = "-Y_gpp"
value_fno_exception = "-fno-exception"
value_stdlib = "-stdlib=libstdc++"
value_fno_rtti = "-fno-rtti"

value_Optimisation_three = "-O3"
value_Optimisation_fast = "-Ofast"

value_qnx = "-D_QNX_"
value_include_path = "-I"
value_library_path = "-L"
value_library_name = "-l"
violations: list = []

def map_targets_label_name_to_action(targets, actions):
    map_targets_name_to_action = {}
    for target in targets:
        action_list = []
        for action in actions:
            if target.id == action.target_id:
                action_list.append(action)

        map_targets_name_to_action[target.label] = action_list

    return map_targets_name_to_action


def log_violation(option_name, str_message):
    violation_dict = {option_name: str_message}
    violations.append(violation_dict)


def check_std_cplus_11_violation(name, options):
    pass


def check_std_cplus_14_violation(name, options):
    pass


def check_std_cplus_17_violation(name, options):
    pass


def check_qnx_source_violation(name, options):
    pass


def check_nostdinc_violation(name, options):
    value_nostdinc_list = [
        current_option
        for current_option in options
        if value_nostdinc in current_option
    ]

    if value_nostdinc_list:
        str_message = f"copts with {value_nostdinc} violation detected"
        log_violation(name, str_message)
        print(str_message)


def check_y_gpp_violation(name, copts):
    pass


def check_fno_exception_violation(name, copts):
    pass


def check_stdlib_violation(name, copts):
    pass


def check_fno_rtti_violation(name, copts):
    pass


def check_override_include_path_violation(name, copts):
    pass


def check_compiler_violations_for_libcxx(name, copts):
    check_nostdinc_violation(name, copts)
    check_std_cplus_17_violation(name, copts)
    check_y_gpp_violation(name, copts)
    check_fno_exception_violation(name, copts)
    check_stdlib_violation(name, copts)
    check_fno_rtti_violation(name, copts)
    check_override_include_path_violation(name, copts)


def check_nostdinc_cplus_violation(name, copts):
    pass


def check_compiler_violations_for_libc(name, copts):
    check_nostdinc_cplus_violation(name, copts)
    check_std_cplus_11_violation(name, copts)
    check_std_cplus_14_violation(name, copts)
    check_std_cplus_17_violation(name, copts)
    check_qnx_source_violation(name, copts)


def check_catalog_violation(name, linkopts):
    pass


def check_nostdlib_violation(name, linkopts):
    pass


def check_override_library_path_violation(name, linkopts):
    pass


def check_override_library_name_violation(name, linkopts):
    pass


def check_linker_violations_for_libcxx(name, linkopts):
    check_catalog_violation(name, linkopts)
    check_nostdlib_violation(name, linkopts)
    check_override_library_path_violation(name, linkopts)
    check_override_library_name_violation(name, linkopts)


def check_nostdlib_cplus_violation(name, linkopts):
    pass


def check_linker_violations_for_libc(name, linkopts):
    check_nostdlib_cplus_violation(name, linkopts)


def find_violation(targets):
    for name, actions in targets.items():
        # print('name {}, actions {} '.format(name, actions))

        for action in actions:
            is_cplus_file = True
            is_c_file = True
            use_cplus_rule = True
            if action.mnemonic == 'CppCompile':
                copts = action.arguments

                length = len(copts)
                if copts[length - 4] == "-c":
                    filename = copts[length - 3]
                    print('file name is  {}'.format(filename))

                    # if file name is .cc, .cpp or .hpp
                    filename_split = filename.split('.')
                    if len(filename_split) == 2:
                        ext = filename_split[1]

                        if ext == "cc" or ext == "cpp" or ext == "hpp":
                            check_compiler_violations_for_libcxx(option_copts, copts)
                            continue

                        if ext == "c":
                            check_compiler_violations_for_libcxx(option_copts, copts)
                            use_cplus_rule = False
                            continue

                        if is_cplus_file and not is_c_file:  # default
                            check_compiler_violations_for_libcxx(option_copts, copts)

            if action.mnemonic == 'CppLink':
                linkopts = action.arguments
                print(linkopts)

                if use_cplus_rule:
                    check_linker_violations_for_libcxx(option_linkopts, linkopts)

                else:
                    check_linker_violations_for_libc(option_linkopts, linkopts)


def scan_violations():
    # Use a breakpoint in the code line below to debug your script.
    action_graph = analysis_v2_pb2.ActionGraphContainer()
    try:
        with open("hello_world_encoded", "rb") as f:
            action_graph.ParseFromString(f.read())

            actions = action_graph.actions
            targets = action_graph.targets

            mapped_targets = map_targets_label_name_to_action(targets, actions)

            # for each mapped targets now check violations
            find_violation(mapped_targets)

    except Exception as ex:
        print('error in scan_violations: ' + str(ex))
        traceback.print_exc()


if __name__ == '__main__':
    scan_violations()
