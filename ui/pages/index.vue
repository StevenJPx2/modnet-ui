<script setup lang="ts">
const file = ref<File | Blob>();
const fileData = ref<string>("");
const url = useObjectUrl(file);
const user = useSupabaseUser();
const loading = computed(() => fileData.value === "");

function _arrayBufferToBase64(buffer: ArrayBufferLike) {
  var binary = "";
  var bytes = new Uint8Array(buffer);
  var len = bytes.byteLength;
  for (var i = 0; i < len; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return window.btoa(binary);
}

const { files, open, reset } = useFileDialog({
  multiple: false,
  accept: "jpeg, jpg",
});

watch(files, async (val) => {
  file.value = (val ?? [])[0];

  const arrayBuffer = await file.value?.arrayBuffer();

  try {
    const { data } = await useFetch<string>(
      "https://process-image-harrehuwdq-et.a.run.app",
      {
        method: "POST",
        body: arrayBuffer,
        headers: { "Content-Type": file.value!.type },
      }
    );

    await useFetch<{ error: string }>("/api/insertPicture", {
      method: "POST",
      body: {
        entry_image: _arrayBufferToBase64(arrayBuffer),
        converted_image: data.value!,
        image_type: file.value!.type,
        user_email: user.value!.email,
      },
    });

    fileData.value = data.value!;
  } catch (e) {
    console.error(e);
  }
});
</script>

<template>
  <div>
    <button class="btn mb-3" type="button" @click="open()">Upload file</button>
    <br />
    <div class="flex flex-wrap gap-4">
      <img class="img" v-if="file !== null" :src="url" alt="" />
      <div
        v-if="loading && file"
        class="img aspect-square bg-slate-300 animate-pulse"
      />
      <img
        class="img"
        v-else-if="!loading"
        :src="`data:${file?.type};base64,${fileData}`"
        alt=""
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.img {
  @apply h-96;
  @apply rounded-lg;
  @apply object-cover;
}
</style>
