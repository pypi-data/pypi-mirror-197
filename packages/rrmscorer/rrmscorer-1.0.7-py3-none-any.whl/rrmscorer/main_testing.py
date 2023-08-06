# Example:
# python -m rrmscorer ...

import sys, os
import json

if __name__ == '__main__':
    _command, *parameters = sys.argv
    print("RRMScorer - Command Line Interface")

    tools = []
    fileName = None
    outputFileName = None
    identifier = None

    for index, param in enumerate(parameters):
        if param == "--help" or param == "-h":
          pass
        if param == "-file":
          fileName = parameters[index + 1]
        if param == "-UP":
          identifier = parameters[index + 1]
        if param == "-ws":
            ws = parameters[index + 1]
        if param == "-RNA":
          rna_seq = parameters[index + 1]
        if param == "-top":
            top = True
        if param == "-plot":
            plot = True

    if len(tools) == 0:
        exit("At least one predictor should be present: -agmata, -dynamine, -disomine, -efoldmine")
    if not fileName:
        exit("An input file is required: -file /path/to/file")
    if not outputFileName:
        exit("An output file path is required: -output /path/to/output_file.json")
    if not identifier:
        exit("An identifier is required: -identifier name")

    output_filepath = os.path.realpath(outputFileName)

    print("Ready to execute predictions with these arguments:\n{0}\n{1}\n{2}\n{3}\n{4}".format(fileName, outputFileName, output_filepath, identifier, tools))

    single_seq = SingleSeq(fileName).predict(tools)
    print("All predictions have been executed. Next step: exporting the results")
    json = single_seq.get_all_predictions_json(identifier)

    print("All predictions have been exported. Next step: saving json inside output path: {0}".format(output_filepath))

    with open(output_filepath, 'w', encoding="utf-8") as json_output_file:
        json_output_file.write(json)

    exit(0)