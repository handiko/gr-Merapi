INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_MERAPI Merapi)

FIND_PATH(
    MERAPI_INCLUDE_DIRS
    NAMES Merapi/api.h
    HINTS $ENV{MERAPI_DIR}/include
        ${PC_MERAPI_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    MERAPI_LIBRARIES
    NAMES gnuradio-Merapi
    HINTS $ENV{MERAPI_DIR}/lib
        ${PC_MERAPI_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(MERAPI DEFAULT_MSG MERAPI_LIBRARIES MERAPI_INCLUDE_DIRS)
MARK_AS_ADVANCED(MERAPI_LIBRARIES MERAPI_INCLUDE_DIRS)

