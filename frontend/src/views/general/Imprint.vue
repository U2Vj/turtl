<script setup lang="ts">
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
</script>

<template>
  <DefaultLayout>
    <template #heading>Imprint</template>
    <template #default>
      <p>
        Project Title: TURTL<br />
        Institution: Fachhochschule Dortmund - University of Applied Sciences and Arts<br />
        Department: Informatik<br />
        Project Supervisors: Prof. Dr. Holger Schmidt<br />
        <br />
        Contact Information:<br />
        Fachhochschule Dortmund<br />
        Sonnenstraße 96-100<br />
        44139 Dortmund, Germany<br />
      </p>
      <br />
      <p>
        Legal Form: The Fachhochschule Dortmund is a public corporation.<br />
        Regulatory Authority: Ministry of Culture and Science of the State of North Rhine-Westphalia
        (MKW NRW)<br />
        VAT Identification Number: DE [Number]<br />
      </p>
      <br />
      <p>
        Disclaimer: The content of this project has been carefully prepared and reviewed. However,
        the Fachhochschule Dortmund does not guarantee the accuracy, completeness, or quality of the
        information provided.<br />
      </p>
      <br />
      <p>
        Copyright: © 2026, Fachhochschule Dortmund. All rights reserved. All content within the
        project, including texts, graphics, and images, is protected by copyright and may not be
        reproduced without the express permission of the Fachhochschule Dortmund.<br />
      </p>
    </template>
  </DefaultLayout>
</template>

<style scoped>
.indented-list {
  padding-left: 2em;
}
</style>
