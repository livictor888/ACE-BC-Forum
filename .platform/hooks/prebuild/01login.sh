#!/bin/bash
USER=`/opt/elasticbeanstalk/bin/get-config environment -k USER`
/opt/elasticbeanstalk/bin/get-config environment -k PASSWD | docker login -u $USER --password-stdin