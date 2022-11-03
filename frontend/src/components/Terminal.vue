<template>
    <b-container fluid>
  <b-row>
    <b-col sm="2">
      <label for="textarea-auto-height">Terminal:</label>
    </b-col>
    <b-col sm="10">
      <b-form-textarea
        id="textarea-auto-height"
        rows="40"
        max-rows="100"
      ></b-form-textarea>
    </b-col>
  </b-row>
</b-container>
</template>

<style scoped>
#textarea-auto-height {
  background-color:black;
  color: white;
}
</style>
