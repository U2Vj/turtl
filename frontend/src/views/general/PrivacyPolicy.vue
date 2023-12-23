<script setup lang="ts">
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
</script>

<template>
  <DefaultLayout>
    <template #heading>Privacy Policy</template>
    <template #default>
      <!-- Introduction Section -->
      <h2>Introduction</h2>
      <p>
        This Privacy Policy applies to TURTL and sets out our policy on the gathering and use of
        information on this site and our other sites.
      </p>

      <br />
      <!-- Collection of Information Section -->
      <h2>Collection of Information</h2>
      <p>We collect various types of information, including:</p>
      <ul class="indented-list">
        <li>Personally Identifiable Information (PII) such as names and email addresses.</li>
        <li>
          Non-Personally Identifiable Information (NPII) such as browser type, operating system, and
          IP address.
        </li>
      </ul>

      <br />
      <!-- Use of Information Section -->
      <h2>Use of Information</h2>
      <p>The information we collect is used to:</p>
      <ul class="indented-list">
        <li>Provide and improve our services.</li>
        <li>Communicate with you about your account or transactions with us.</li>
        <li>Provide customer service.</li>
        <li>Perform research and analysis about your use of, or interest in, our services.</li>
      </ul>

      <br />
      <!-- Sharing of Information Section -->
      <h2>Sharing of Information</h2>
      <p>We may share your information with third parties:</p>
      <ul class="indented-list">
        <li>
          In the event of a corporate sale, merger, reorganization, dissolution, or similar event.
        </li>
        <li>When required by law or to respond to legal process.</li>
        <li>To protect our rights, as well as those of our users or others.</li>
      </ul>

      <br />
      <!-- Security Section -->
      <h2>Security</h2>
      <p>
        We implement reasonable security measures to safeguard the confidentiality of your personal
        information.
      </p>

      <br />
      <!-- Your Privacy Rights Section -->
      <h2>Your Privacy Rights</h2>
      <p>You have the right to:</p>
      <ul class="indented-list">
        <li>Access personal information we hold about you.</li>
        <li>Request the correction of inaccurate information.</li>
        <li>Request the deletion of your personal information.</li>
        <li>Object to the processing of your data.</li>
      </ul>

      <br />
      <!-- Changes to This Privacy Policy Section -->
      <h2>Changes to This Privacy Policy</h2>
      <p>We may update this Privacy Policy from time to time.</p>

      <br />
      <!-- Contact Us Section -->
      <h2>Contact Us</h2>
      <p>
        If you have any questions or concerns about our privacy practices, please contact us at HSD.
      </p>
    </template>
  </DefaultLayout>
</template>

<style scoped>
.indented-list {
  padding-left: 2em;
}
</style>
