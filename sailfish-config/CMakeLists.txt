cmake_minimum_required(VERSION 3.10)
project(sailfish_rsnapshot_user_config
        VERSION 1.0
        LANGUAGES NONE
        DESCRIPTION "Sailfish rsnapshot User Config"
)

include(GNUInstallDirs)

option(DEFAULTUSER_ENABLE "Enable user defaultuser" ON)
option(NEMO_ENABLE        "Enable user nemo"        ON)

if(DEFAULTUSER_ENABLE)
        list(APPEND Users "defaultuser")
endif()
if(NEMO_ENABLE)
        list(APPEND Users "nemo")
endif()

foreach(USER ${Users})
        configure_file(rsnapshot.conf.sailfish_user.in rsnapshot.conf.sailfish_${USER} @ONLY)
        list(APPEND ADDITIONAL_CLEAN_FILES rsnapshot.conf.sailfish_${USER})
        install(FILES rsnapshot.conf.sailfish_${USER} DESTINATION ${CMAKE_INSTALL_FULL_SYSCONFDIR})
endforeach()

configure_file(rsnapshot.conf.sailfish_lvm.in rsnapshot.conf.sailfish_root_lvm @ONLY)
install(FILES rsnapshot.conf.sailfish_root_lvm DESTINATION ${CMAKE_INSTALL_FULL_SYSCONFDIR})
list(APPEND ADDITIONAL_CLEAN_FILES rsnapshot.conf.sailfish_root_lvm)

# config files referenced by the above:
install(FILES home_default.exclude rootfs_default.exclude
        DESTINATION ${CMAKE_INSTALL_FULL_SYSCONFDIR}/rsnapshot/
)

install(FILES
        rsnapshot-user@.service
        rsnapshot-user-daily.timer
        rsnapshot-user-monthly.timer
        rsnapshot-user-weekly.timer
        DESTINATION ${CMAKE_INSTALL_PREFIX}/lib/systemd/user/
)

