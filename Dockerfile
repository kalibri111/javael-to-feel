# Source project must contains:
# -2 empty(!) py-package:
#     ANTLR_FEELParser
#     ANTLR_JavaELParser
# -example
# -gen
# -src
# -test(optional?)
# -tree_examples(optional?)

FROM python:3.9

# copy project files from host to container
COPY . /usr/src/app/
WORKDIR /usr/src/app/

# install python dependencies
RUN pip3 install -r requirements.txt

# TODO: need to add input_path and output_path
WORKDIR /usr/src/app/src/document_info_table
ENTRYPOINT ["python3", "./report.py", "/usr/src/app/input/example.xml", "/usr/src/app/output"]
