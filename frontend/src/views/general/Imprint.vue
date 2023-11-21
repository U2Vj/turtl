<script setup lang="ts">
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
</script>

<template>
  <DefaultLayout>
    <template #heading>Imprint</template>
    <template #default>
      <p>
        Project Title: TURTL<br />
        Institution: Hochschule Düsseldorf - University of Applied Sciences<br />
        Department: Medieninformatik<br />
        Project Supervisors: Prof. Dr. Holger Schmidt, Prof. Dr.-Ing. M.Sc. Markus Dahm<br />
        <br />
        Contact Information:<br />
        Hochschule Düsseldorf<br />
        University of Applied Sciences<br />
        Münsterstraße 156<br />
        40476 Düsseldorf, Germany<br />
      </p>
      <br />
      <p>
        Legal Form: The Hochschule Düsseldorf is a public corporation.<br />
        Regulatory Authority: Ministry of Culture and Science of the State of North Rhine-Westphalia
        (MKW NRW)<br />
        VAT Identification Number: DE [Number]<br />
      </p>
      <br />
      <p>
        Disclaimer: The content of this project has been carefully prepared and reviewed. However,
        the Hochschule Düsseldorf does not guarantee the accuracy, completeness, or quality of the
        information provided.<br />
      </p>
      <br />
      <p>
        Copyright: © 2023, Hochschule Düsseldorf. All rights reserved. All content within the
        project, including texts, graphics, and images, is protected by copyright and may not be
        reproduced without the express permission of the Hochschule Düsseldorf.<br />
      </p>
    </template>
  </DefaultLayout>
</template>

<style scoped>
.indented-list {
  padding-left: 2em;
}
</style>
