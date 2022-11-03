<template>
    <div>
      <b-form @submit="onSubmit" @reset="onReset" v-if="show">
        <b-form-group
          id="title-input-group"
          label="Titel:"
          label-for="title-input"
          description="Der Name des Klassenraums. Dieser wird den anderen Benutzern angezeigt."
        >
          <b-form-input
            id="title-input"
            v-model="form.title"
            type="text"
            placeholder="Gib einen Titel an"
            required
          ></b-form-input>
        </b-form-group>

        <b-form-group id="description-input-group" label="Beschreibung:" label-for="description-input" description="Beschreibe diesen Klassenraum.">
          <b-form-textarea
            id="description-input"
            type="text"
            v-model="form.description"
            placeholder="Gib einen beschreibenden Text an"
            required
          ></b-form-textarea>
        </b-form-group>

        <b-form-group id="semestre-input-group" label="Semester:" label-for="semestre-input" description="An Studierende welches Semesters richtet sich der Klassenraum?">
          <b-form-input
            id="semestre-input"
            v-model="form.semestre"
            placeholder="Gib ein Semester an"
            required
          ></b-form-input>
        </b-form-group>

       <b-form-group id="student-input-group" label="Studenten:" label-for="student-input" description="An welche Studenten richtet sich der Klassenraum?">
          <b-form-input
            id="student-input"
            v-model="form.student"
            placeholder="Studenten"
            required
          ></b-form-input>
          </b-form-group>

        <b-form-group id="environment-input-group" label="Environment">
            <b-form-file
                v-model="form.environment"
                :state="Boolean(form.environment)"
                placeholder="Lade eine Docker-Datei hoch..."
                drop-placeholder="Docker-Datei einfügen..."
            ></b-form-file>
            <div class="mt-3">Ausgewählt: {{ form.environment? form.environment.name : '' }}</div>
        </b-form-group>

        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </div>
  </template>

<script>
export default {
    data () {
        return {
            form: {
                title: '',
                description: '',
                semestre: '',
                student: '',
                environment: null
            },
            show: true
        }
    },
    methods: {
        onSubmit (event) {
            event.preventDefault()
            alert(JSON.stringify(this.form))
        },
        onReset (event) {
            event.preventDefault()
            // Reset our form values
            this.form.titel = ''
            this.form.description = ''
            this.form.semestre = ''
            this.form.student = ''
            this.form.environment = null
            // Trick to reset/clear native browser form validation state
            this.show = false
            this.$nextTick(() => {
                this.show = true
            })
        }
    }
}
</script>
