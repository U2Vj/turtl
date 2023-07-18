<script setup lang="ts">
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
import PrimaryButton from '@/components/layouts/PrimaryButton.vue'
import { ref } from 'vue'

const classrooms = ref([
  {
    id: '1',
    classroom: 'Man in the Middle',
    role: 'Attack',
    memberCount: 12,
    description:
      'This course explores Man in the Middle attacks and the various ways in which they can be executed. Topics include eavesdropping, session hijacking, and SSL stripping.'
  },
  {
    id: '2',
    classroom: 'Computer Networks',
    role: 'Defense',
    memberCount: 31,
    description:
      'This course covers the principles and technologies that enable computers and devices to communicate and share resources. Topics include network architecture, protocols, and network security.'
  },
  {
    id: '3',
    classroom: 'Firewall',
    role: 'Attack',
    memberCount: 22,
    description:
      'This course focuses on network security and the role of firewalls in protecting against cyber attacks. Topics include firewall types, configurations, and best practices.'
  },
  {
    id: '4',
    classroom: 'Encryption',
    role: 'Defense',
    memberCount: 18,
    description:
      'This course introduces the principles and techniques of encryption and how it is used to secure data. Topics include symmetric and asymmetric encryption, hashing, and digital signatures.'
  },
  {
    id: '5',
    classroom: 'Cyber Attacks',
    role: 'Attack',
    memberCount: 26,
    description:
      'This course examines the various types of cyber attacks and the methods used by attackers to gain unauthorized access to computer systems and networks. Topics include phishing, malware, and social engineering.'
  },
  {
    id: '6',
    classroom: 'VPN',
    role: 'Defense',
    memberCount: 8,
    description:
      'This course focuses on Virtual Private Networks (VPNs) and their role in secure communication over the internet. Topics include VPN protocols, encryption, and deployment.'
  },
  {
    id: '7',
    classroom: 'Authentication',
    role: 'Defense',
    memberCount: 14,
    description:
      'This course covers the principles of authentication and the various methods used to verify the identity of users, devices, and systems. Topics include password policies, two-factor authentication, and biometric authentication.'
  },
  {
    id: '8',
    classroom: 'Intrusion Detection and Prevention',
    role: 'Defense',
    memberCount: 20,
    description:
      'This course examines the various methods used to detect and prevent intrusions into computer systems and networks. Topics include intrusion detection systems, intrusion prevention systems, and security information and event management (SIEM).'
  },
  {
    id: '9',
    classroom: 'Malware',
    role: 'Attack',
    memberCount: 29,
    description:
      'This course focuses on malware and its role in cyber attacks. Topics include virus, worm, and Trojan horse attacks, rootkits, and backdoors. Students will learn how to identify and remove malware.'
  },
  {
    id: '10',
    classroom: 'Access Control',
    role: 'Defense',
    memberCount: 11,
    description:
      'This course covers the principles and techniques of access control and how they are used to protect computer systems and networks. Topics include access control models, access control policies, and access control lists.'
  },
  {
    id: '11',
    classroom: 'Network Monitoring',
    role: 'Defense',
    memberCount: 23,
    description:
      'This course examines the various tools and techniques used to monitor computer networks for performance and security issues. Topics include network monitoring tools, traffic analysis, and anomaly detection.'
  },
  {
    id: '12',
    classroom: 'Cybersecurity',
    role: 'Defense',
    memberCount: 37,
    description:
      'This course provides a comprehensive overview of cybersecurity and the methods used to protect computer systems, networks, and devices from cyber attacks. Topics include risk assessment, security policies, incident response, and disaster recovery.'
  }
])
</script>

<template>
  <DefaultLayout>
    <template #heading>My Classrooms</template>
    <template #postHeadingButton>
      <PrimaryButton buttonName="Create Classroom"> </PrimaryButton>
    </template>
    <template #default>
      <v-row class="mt-5">
        <v-col v-for="classroom in classrooms" :key="classroom.id" cols="12" xs="12" sm="6" md="4">
          <v-card :key="classroom.id" variant="flat" color="cardColor" class="elevation-4">
            <v-card-title :title="classroom.classroom">
              {{ classroom.classroom }}
            </v-card-title>
            <v-card-text>
              <p class="d-flex justify-space-between">
                <span class="d-flex align-center">
                  <v-icon icon="mdi-sword" class="mr-1" v-if="classroom.role === 'Attack'"></v-icon>
                  <v-icon
                    icon="mdi-shield"
                    class="mr-1"
                    v-else-if="classroom.role === 'Defense'"
                  ></v-icon>
                  <v-icon icon="mdi-school" class="mr-1" v-else></v-icon>
                  Role: {{ classroom.role }}
                </span>
                <span class="d-flex align-center">
                  <v-icon icon="mdi-account-group" class="mr-1"></v-icon>
                  {{ classroom.memberCount }} members
                </span>
              </p>
              <p v-text="classroom.description" class="classroomDescription mt-4 text-justify"></p>
            </v-card-text>
            <v-card-actions>
              <v-btn variant="tonal" color="primary" class="d-flex flex-fill elevation-2"
                >Visit Classroom</v-btn
              >
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </template>
  </DefaultLayout>
</template>

<style scoped>
.classroomDescription {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  -webkit-line-clamp: 5;
  height: 100px;
  line-height: 20px;
}
</style>
