<template>
  <div>
    <input type="file" id="file" ref="file" v-on:change="upload()" />
    <div id="message">{{ task_message }}</div>
  </div>
</template>

<script>
import axios from "axios";

const url = "http://localhost:5000/api";

export default {
  data() {
    return {
      task_message: "fff",
    };
  },
  methods: {
    upload: function() {
      axios
        .get(`${url}/predict`)
        .then(
          (response) =>
            (this.task_message = `task ${response.data.task_id} enqueued`)
        );
    },
  },
};
</script>

<style scoped>
#message {
  margin-top: 5em;
  font-size: 2em;
}
</style>
