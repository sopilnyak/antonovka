<template>
  <div>
    <div id="results">
      <div class="button-wrapper">
        <button class="button">Загрузить фото</button>
        <input type="file" id="file" ref="file" v-on:change="upload()" />
      </div>
      <div
        v-for="task in tasks.slice().reverse()"
        class="image"
        :key="task.taskId"
        :style="{
          backgroundImage: 'url(' + task.imageUrl + ')',
          borderColor: borderColor(task.result),
          opacity: imageOpacity(task.result),
        }"
      >
        <div class="spinner-wrapper">
          <div
            class="spinner"
            :style="{
              visibility: task.result == null ? 'visible' : 'hidden',
            }"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

const url = "http://localhost:5000/api";

class Task {
  constructor(taskId, imageUrl) {
    this.taskId = taskId;
    this.imageUrl = imageUrl;
    this.result = null;
  }
}

export default {
  data() {
    return {
      tasks: [],
    };
  },
  methods: {
    upload: function() {
      this.file = this.$refs.file.files[0];
      let formData = new FormData();
      formData.append("file", this.file);
      this.$refs.file.value = null;
      axios
        .post(`${url}/predict`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          let imageUrl = `${url}/image/${response.data.filename}`;
          this.tasks.push(new Task(response.data.task_id, imageUrl));
          setTimeout(
            (taskId) => this.getTaskResult(taskId),
            1000,
            response.data.task_id
          );
        });
    },

    getTaskResult: function(taskId) {
      axios.get(`${url}/${taskId}/status`).then((response) => {
        if (response.data.result != "") {
          let task = this.tasks.find((value) => value.taskId == taskId);
          task.result = response.data.result;
        } else {
          setTimeout((taskId) => this.getTaskResult(taskId), 1000, taskId);
        }
      });
    },

    borderColor: function(taskResult) {
      if (taskResult == null) {
        return "gray";
      }
      if (taskResult == "true") {
        return "red";
      }
      return "green";
    },

    imageOpacity: function(taskResult) {
      return taskResult == null ? 0.3 : 1;
    },
  },
};
</script>

<style scoped>
#results {
  font-size: 2em;
  width: 70%;
  min-width: 20em;
  margin: 2em auto;
}

.image {
  display: inline-block;
  width: 6em;
  height: 6em;
  margin: 0.3em;
  border: 5px solid;
  background-position: center center;
  background-size: cover;
  box-shadow: 0px 0px 33px -7px #5e5e5e;
}

.button-wrapper {
  display: inline-block;
  width: 6em;
  height: 6em;
  margin: 0.3em;
  border: 5px gray dashed;
  background-position: center center;
  background-size: cover;
  position: relative;
  overflow: hidden;
  box-shadow: 0px 0px 33px -7px #5e5e5e;
}

.button {
  background-color: white;
  padding: 40% 20px;
  border: 0;
  font-size: 20px;
  font-weight: bold;
}

.button-wrapper input[type="file"] {
  height: 6em;
  font-size: 100px;
  position: absolute;
  left: 0;
  top: 0;
  opacity: 0;
}

.spinner-wrapper {
  width: 6em;
  height: 6em;
}

.spinner {
  margin: 30% auto;
  height: 60px;
  width: 60px;
  -webkit-animation: rotation 0.6s infinite linear;
  -moz-animation: rotation 0.6s infinite linear;
  -o-animation: rotation 0.6s infinite linear;
  animation: rotation 0.6s infinite linear;
  border-left: 6px solid rgba(0, 174, 239, 0.15);
  border-right: 6px solid rgba(0, 174, 239, 0.15);
  border-bottom: 6px solid rgba(0, 174, 239, 0.15);
  border-top: 6px solid rgba(0, 174, 239, 1);
  border-radius: 100%;
}

@-webkit-keyframes rotation {
  from {
    -webkit-transform: rotate(0deg);
  }
  to {
    -webkit-transform: rotate(359deg);
  }
}
@-moz-keyframes rotation {
  from {
    -moz-transform: rotate(0deg);
  }
  to {
    -moz-transform: rotate(359deg);
  }
}
@-o-keyframes rotation {
  from {
    -o-transform: rotate(0deg);
  }
  to {
    -o-transform: rotate(359deg);
  }
}
@keyframes rotation {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(359deg);
  }
}
</style>
