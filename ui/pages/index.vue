<script setup lang="ts">
const file = ref<File | Blob>();
const fileData = ref<string>("");
const url = useObjectUrl(file);
const { base64 } = useBase64(fileData);

const { files, open, reset } = useFileDialog({
  multiple: false,
  accept: "jpeg, jpg",
});

watch(files, async (val) => {
  file.value = (val ?? [])[0];

  try {
    const { data } = await useFetch<string>("http://127.0.0.1:8080", {
      method: "POST",
      body: await file.value?.arrayBuffer(),
      headers: { "Content-Type": file.value!.type },
    });
    fileData.value = data.value!;
  } catch (e) {
    console.error(e);
  }
});
</script>

<template>
  <div>
    <button type="button" @click="open()">Upload file</button> <br />
    <div class="flex gap-4">
      <img
        class="h-96 rounded-lg object-cover"
        v-if="file !== null"
        :src="url"
        alt=""
      />
      <img
        class="h-96 rounded-lg object-cover"
        v-if="fileData !== ''"
        :src="`data:${file?.type};base64,${fileData}`"
        alt=""
      />
    </div>
  </div>
</template>
