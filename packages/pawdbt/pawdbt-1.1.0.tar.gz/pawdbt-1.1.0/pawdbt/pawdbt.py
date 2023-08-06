#!/usr/bin/env python
# coding: utf-8

from pawdbt.pawdbt_helper_modules import *

def main_yaml():
    try:
        if is_dbt_project_healthy():
            clear_terminal()
            cd = get_current_dir()
            dry_arr = get_all_dry_doc_blocks(cd)
            flag_values = return_flag_values(flag_list)
            selector = ' '.join(flag_values.get('select', None))
            doc_blocks_in_relation = flag_values.get('save-doc-blocks-in', None)

            if doc_blocks_in_relation is not None:
                doc_blocks_in_relation = doc_blocks_in_relation[0]

            always_overwrite = flag_values.get('always-overwrite', False)
            run_models = flag_values.get('run-models', False)
            header_and_info(selector, doc_blocks_in_relation, always_overwrite, run_models)

            if run_models:
                with Halo(text='Creating Models...', spinner=loader):
                    run_selector(selector)

            with Halo(text='Loading Models...', spinner=loader):
                selected_models = get_models_by_identifier_type('name', selector)
                selected_paths = get_models_by_identifier_type('path', selector)

            ymls = []
            mds = []

            with tqdm(total=len(selected_models), colour='green') as pbar:
                for i in range(len(selected_models)):
                    pbar.set_description(f'Gathering Relations Columns ({selected_models[i]})')

                    columns, types = get_relation_columns_and_datatype(selected_models[i])
                    yml = create_relation_yml(selected_models[i], selected_paths[i], columns, dry_arr, types)
                    md = create_relation_md(selected_models[i], selected_paths[i], selected_models, selected_paths, dry_arr, doc_blocks_in_relation)

                    ymls.append(yml)
                    mds.append(md)

                    pbar.update()

            with tqdm(total=len(selected_models), colour='green') as pbar:
                for i in range(len(selected_models)):
                    create_file(selected_paths[i], 'yml', ymls[i], always_overwrite)
                    create_file(selected_paths[i], 'md', mds[i], always_overwrite)

                    pbar.update()

    except Exception as error_str:
        raise_error(error_str)

if __name__ == "__main__":
    main_yaml()
