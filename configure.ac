AC_INIT([ailurus], [10.03], [homer.xing@gmail.com])

AM_INIT_AUTOMAKE

#AM_PROG_CC_C_O

AM_PATH_PYTHON([2.5])
if test "x$PYTHON" = "x:"; then
    AC_MSG_ERROR([Require Python 2.5])
fi
AC_SUBST(PYTHON)

#FIXME: There is a bug.
#PKG_CHECK_MODULES( AILURUS,
#    pygtk-2.0               >= 2.10
#    pygobject-2.0           >= 2.10
#)

GETTEXT_PACKAGE=ailurus
AC_SUBST(GETTEXT_PACKAGE)
AC_DEFINE_UNQUOTED([GETTEXT_PACKAGE],["$GETTEXT_PACKAGE"], [gettext_package])
AM_GNU_GETTEXT([external])
AM_GNU_GETTEXT_VERSION([0.17])

AC_DEFUN([AS_AC_EXPAND],
[
  EXP_VAR=[$1]
  FROM_VAR=[$2]

  dnl first expand prefix and exec_prefix if necessary
  prefix_save=$prefix
  exec_prefix_save=$exec_prefix

  dnl if no prefix given, then use /usr/local, the default prefix
  if test "x$prefix" = "xNONE"; then
    prefix="$ac_default_prefix"
  fi
  dnl if no exec_prefix given, then use prefix
  if test "x$exec_prefix" = "xNONE"; then
    exec_prefix=$prefix
  fi

  full_var="$FROM_VAR"
  dnl loop until it doesn't change anymore
  while true; do
    new_full_var="`eval echo $full_var`"
    if test "x$new_full_var" = "x$full_var"; then break; fi
    full_var=$new_full_var
  done

  dnl clean up
  full_var=$new_full_var
  AC_SUBST([$1], "$full_var")

  dnl restore prefix and exec_prefix
  prefix=$prefix_save
  exec_prefix=$exec_prefix_save
])

AS_AC_EXPAND(DATADIR, "${datadir}")
AS_AC_EXPAND(DATADIR, "${DATADIR}")

AC_CONFIG_FILES([
    Makefile
    src/Makefile
    src/z_locale.py
    src/common/Makefile
    src/gnome/Makefile
    src/fedora/Makefile
    src/ubuntu/Makefile
    data/Makefile
    data/files/Makefile
    data/other_icons/Makefile
    data/suyun_icons/Makefile
    data/umut_icons/Makefile
    data/appicons/Makefile
    data/nautilus_screenshot/Makefile
    data/nautilus_screenshot/es/Makefile
    data/nautilus_screenshot/zh_CN/Makefile
    shortcut/Makefile
    shortcut/ailurus.desktop
    dbus/Makefile
    dbus/cn.ailurus.service
    policykit0/Makefile
    policykit1/Makefile
])

AC_OUTPUT
