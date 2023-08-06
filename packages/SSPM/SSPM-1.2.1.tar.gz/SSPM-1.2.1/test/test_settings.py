TEST_CONFIG = {
    "attributes": ["test_attr"]
}

TEST_IMAGE = [[
    [[255],  [255],  [255]],
    [[255],  [255],  [255]],
    [[255],  [255],  [255]]
]]

TEST_LABEL = '{ ' \
             '"frame_num": 1, ' \
             '"frame_timestamp": ' \
             '"2019-09-12T22:16:01.612000", ' \
             '"frame_priority": -1, ' \
             '"frame_is_quality_controlled": false, ' \
             '"excluded_frame_labeling": false, ' \
             '"excluded_frame_scoring": false, ' \
             '"excluded_targets": [], ' \
             '"excluded_areas": [],' \
             '"objects": {' \
                '"2031": {' \
                    '"object_id": "2031", ' \
                    '"object_class": "SIL_BMP_FRONT", ' \
                    '"object_ontology": "", ' \
                    '"object_extension": "", ' \
                    '"visible_bb_x": -1, ' \
                    '"visible_bb_y": -1, ' \
                    '"visible_bb_width": -1, ' \
                    '"visible_bb_height": -1, ' \
                    '"full_bound_bb_x": 317, ' \
                    '"full_bound_bb_y": 298, ' \
                    '"full_bound_bb_width": 28, ' \
                    '"full_bound_bb_height": 20, ' \
                    '"object_centroid_x": 331, ' \
                    '"object_centroid_y": 308, ' \
                    '"inside_bb_average_pixel_value": -1, ' \
                    '"outside_bb_average_pixel_value": -1, ' \
                    '"inside_bb_stdev_pixel_value": -1, ' \
                    '"outside_bb_stdev_pixel_value": -1, ' \
                    '"is_high_fidelity": false, ' \
                    '"object_is_obscured": false, ' \
                    '"object_obscuration_percentage": -1.0, ' \
                    '"object_is_occluded": false, ' \
                    '"object_occlusion_percentage": -1.0, ' \
                    '"object_obscuration_level": "", ' \
                    '"object_occlusion_level": "", ' \
                    '"edge_of_frame": false, ' \
                    '"labeled_datetime_utc": "", ' \
                    '"labeler_type": "", ' \
                    '"labeler_name": "", ' \
                    '"quality_controlled_datetime_utc": "", ' \
                    '"quality_controller_name": ""}}' \
             '}'

TEST_META = '{' \
            '"object_id": "",' \
            '"data_name": "sensor_yaw",' \
            '"data_source": "",' \
            '"data_references": "",' \
            '"measurement_units": "",' \
            '"sync_variable_type": "frame_timestamp",' \
            '"has_been_synchronized": true,' \
            '"interpolation_algorithm": "",' \
            '"sync_variable_array": [' \
            '    "2019-09-12T22:16:01.612000",' \
            '    "2019-09-12T22:16:01.645000"' \
            '],' \
            '"measurements": [' \
            '    -24.0,' \
            '    -42.0' \
            '],' \
            '"measurement_known_latency": -1,' \
            '"measurement_uncertainty": "",' \
            '"measurement_standard_deviation": -1.0' \
            '}'

TEST_SYNCH = '{' \
             '"frame_num": 166,' \
             '"frame_timestamp": "2019-09-12T22:16:07.111000",' \
             '"objects": {' \
             '    "2031": {' \
             '        "object_id": "2031",' \
             '        "object_aspect-unknown": 0.0' \
             '    }' \
             '},' \
             '"sensor_yaw-unknown": -55.3114394651648' \
             '}'

TEST_MISC = '{' \
            '"misc_test": 404'\
            '}'
