This module can read, modify, and write a .pbxproj file from an Xcode 4 project.  The file is usually called `project.pbxproj` and can be found inside the .xcodeproj bundle.

**Changes**: What i changed on this library? 

Add method `add_subproject_as_dependency`. You can use this method to add a sub project as dependency. i.e:
    
    if __name__ == "__main__":
      project = XcodeProject.Load("/Users/junwchina/Programs/CPP/TestPlugin/proj.ios_mac/TestPlugin.xcodeproj/project.pbxproj")

      # add library projects
      project.add_subproject_as_dependency("/Users/junwchina/SDK/plugin-x/protocols/proj.ios/PluginProtocol.xcodeproj",
                                           "libPluginProtocol.a",
                                           header_paths = ["/Users/junwchina/SDK/plugin-x/protocols/include"],
                                           sdk_dependencies = ["SystemConfiguration.framework", "StoreKit.framework",
                                                               "GameController.framework", "CoreData.framework"],
                                           dev_dependencies = ["CoreTelephony.framework", "AdSupport.framework",
                                                               "MessageUI.framework", "MediaPlayer.framework"])
      project.add_subproject_as_dependency("/Users/junwchina/SDK/plugin-x/plugins/admob/proj.ios/PluginAdmob.xcodeproj", "libPluginAdmob.a")

      if project.modified:
        project.save()


    

Basic Usage:

    from mod_pbxproj import XcodeProject
    project = XcodeProject.Load('/path/to/.pbxproj')

You now have a project object that has a bunch of methods for manipulating it.  By default files added to the project are also added to the appropriate build phase, as long as the file's type can be determined.

This will add a file in the root of a project.
**NOTE**: everything goes better if you supply absolute paths.

    project.add_file('/path/to/file.name')

This will return a group object that you can add files/folders under

    new_group = project.get_or_create_group('new group')

This will add other.file to the project as a child of 'new group'

    project.add_file('/path/to/other.file', parent=new_group)

If you want to add a framework or library that is found in the SDK,
supply a relative path and set the tree argument to 'SDKROOT'

    project.add_file('System/Libray/UIKit.framework', tree='SDKROOT')
    project.add_file('usr/lib/libz.dylib', tree='SDKROOT')

This will recursively create groups and add the directory's contents
to the project.  You can optionally turn off the recursion.

    project.add_folder('/path/to/folder')

You can supply an array of regular expressions for files you want to skip. This won't add any pdfs or mdown files found as it recurses.

    project.add_folder('/path/to/folder', excludes=["^.*\.mdown$", "^.*\.pdf$"])

If a modification you are trying to apply have already been applied to the project then it will be skipped.  This means that before saving the project you should check the modified flag to make sure changes have occured.

    if project.modified:
        project.backup()
        project.save() # will save by default using the new xcode 3.2 format
        project.save(old_format=True) # will force to save the project in plist XML format (NOT RECOMMENDED)

The backup method saves a copy of the project file in its current state on disk.  This can be very useful if a modification leaves the project file unreadable.

p.s. **NO WARRANTIES**
