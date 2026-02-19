include "dependencies.lua"
include "Premake5/scripts/helpers.lua"

workspace "FlatByte"
    architecture "x64"
    configurations {"Debug", "Release"}
    startproject "FlatByte"

    buildpattern = "%{cfg.buildcfg}.%{cfg.system}.%{cfg.architecture}"

    group "Dependencies"
        include "lib/imgui"
        include "lib/SFML"
        include "lib/prolog"
    group ""

    group "Modules"
        include "module/PrologAPI"
    group ""

    include "game"

    project "FlatByte"
        kind "StaticLib"
        language "C++"
        characterset "MBCS"
        cppdialect "C++17"

        targetdir("build/bin/" .. buildpattern .. "/%{prj.name}")
        objdir("build/int/" .. buildpattern .. "/%{prj.name}")

        files
        {
            "%{wks.location}/include/**.hpp",
            "%{wks.location}/source/**.cpp"
        }

        pchheader "pch.hpp"
        pchsource "%{wks.location}/source/pch.cpp"

        includedirs
        {
            "%{wks.location}/include",
            "%{wks.location}/lib/imgui",
            "%{wks.location}/lib/SFML/SFML/include",
            "%{wks.location}/lib/prolog/prolog/include",
            "%{wks.location}/lib/prolog/prolog/source",
            "%{wks.location}/%{LibraryMap.FMOD.Include}"
        }

        defines
        {
            -- "SFML_STATIC"
        }

        links
        {
            "opengl32.lib",
            "winmm.lib",
            "gdi32.lib",
            "imgui",
            "sfml-system",
            "sfml-window",
            "sfml-graphics",
            "%{wks.location}/lib/prolog/prolog/lib/libswipl.lib",
            "%{wks.location}/%{LibraryMap.FMOD.Any.FMOD_WIN64_FSBANK_LIB}"
        }

        postbuildcommands
        {
            "{COPYFILE} %[%{LibraryMap.FMOD.Any.FMOD_WIN64_FSBANK_DLL}] %[%{cfg.buildtarget.directory}]",
            "{COPYFILE} %[%{LibraryMap.FMOD.Any.FMOD_WIN64_LIBFSVORBIS_DLL}] %[%{cfg.buildtarget.directory}]",
            "{COPYFILE} %[%{LibraryMap.FMOD.Any.FMOD_WIN64_OPUS_DLL}] %[%{cfg.buildtarget.directory}]"
        }

        filter "configurations:Release"
            optimize "on"

            links
            {
                "%{wks.location}/%{LibraryMap.FMOD.Release.FMOD_WIN64_CORE_LIB}",
                "%{wks.location}/%{LibraryMap.FMOD.Release.FMOD_WIN64_STUDIO_LIB}",
            }

            postbuildcommands
            {
                "{COPYFILE} %[%{LibraryMap.FMOD.Release.FMOD_WIN64_CORE_DLL}] %[%{cfg.buildtarget.directory}]",
                "{COPYFILE} %[%{LibraryMap.FMOD.Release.FMOD_WIN64_STUDIO_DLL}] %[%{cfg.buildtarget.directory}]"
            }

        filter "configurations:Debug"
            symbols "on"

            links
            {
                "%{wks.location}/%{LibraryMap.FMOD.Debug.FMOD_WIN64_CORE_LIB}",
                "%{wks.location}/%{LibraryMap.FMOD.Debug.FMOD_WIN64_STUDIO_LIB}",
            }

            postbuildcommands
            {
                "{COPYFILE} %[%{LibraryMap.FMOD.Debug.FMOD_WIN64_CORE_DLL}] %[%{cfg.buildtarget.directory}]",
                "{COPYFILE} %[%{LibraryMap.FMOD.Debug.FMOD_WIN64_STUDIO_DLL}] %[%{cfg.buildtarget.directory}]",
                "{COPYFILE} %[%{LibraryMap.SFML.Debug.SFML_WIN64_SYSTEM_DLL}] %[%{cfg.buildtarget.directory}]",
                "{COPYFILE} %[%{LibraryMap.SFML.Debug.SFML_WIN64_WINDOW_DLL}] %[%{cfg.buildtarget.directory}]",
                "{COPYFILE} %[%{LibraryMap.SFML.Debug.SFML_WIN64_GRAPHICS_DLL}] %[%{cfg.buildtarget.directory}]"
            }