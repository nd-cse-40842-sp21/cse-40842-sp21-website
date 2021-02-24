#!/bin/sh

XML_PATH=$(dirname $0)/../public/rss.xml
YML_PATH=$(dirname $0)/../static/yaml/blogs.yaml

# Update blogs yaml from Googe Spreadsheet
if (cd $(dirname $0) ; ./sheet_to_yaml.py) > ${YML_PATH}.tmp; then
    cp -f ${YML_PATH}.tmp ${YML_PATH}
    rm -f ${YML_PATH}.tmp
fi

# Update planet
if (cd $(dirname $0) ; ./planet.py) > ${XML_PATH}.tmp; then
    cp -f ${XML_PATH}.tmp ${XML_PATH}
    rm -f ${XML_PATH}.tmp
fi

# Push XML
lftp -c "open www3ftps.nd.edu; put -O www/teaching/cse.40842.sp21 ${XML_PATH}"
