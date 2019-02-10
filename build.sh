#!/bin/bash

TOPDIR="/root/rpmbuild"
PROJECT="${CI_PROJECT_DIR}"
SPEC="${CI_PROJECT_NAME}.spec"

if [[ -n ${PRE_BUILDDEP} ]]; then
  bash -c "${PRE_BUILDDEP}"
fi

# Copy all files to SOURCES and .spec to SPECS
cp -va --reflink=auto ${PROJECT}/* "${TOPDIR}/SOURCES/"
cp -va --reflink=auto "${PROJECT}/${SPEC}" "${TOPDIR}/SPECS/"
SPEC="${TOPDIR}/SPECS/${SPEC##*/}"

# Download deps from spec file
yum-builddep -y "${SPEC}"

# List sources
spectool ${SPEC}

# Download sources
spectool -g -R ${SPEC}

# Build the RPMs
rpmbuild -ba ${SPEC}

# Create folder to store artifacts
mkdir -p "${PROJECT}/rpms"
cp -va ${TOPDIR}/{RPMS,SRPMS} ${PROJECT}/rpms/
