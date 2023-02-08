<script setup lang="ts">
definePageMeta({
  middleware: "admin-auth",
});

type PicturesTable = {
  id: string;
  entry_image: string;
  converted_image: string;
  image_type: string;
  user_email: string;
};

const client = useSupabaseClient();
const { data: tableData, pending } = await useLazyAsyncData(
  async () => (await client.from("pictures").select()).data as PicturesTable[]
);
const columns: {
  name: string;
  key: keyof PicturesTable;
  type: "data-url" | "text";
}[] = [
  { name: "ID", key: "id", type: "text" },
  { name: "Entry Image", key: "entry_image", type: "data-url" },
  { name: "Converted Image", key: "converted_image", type: "data-url" },
  { name: "User Email", key: "user_email", type: "text" },
];
</script>

<template>
  <div>
    <div
      v-if="pending"
      class="animate-pulse h-[50vh] w-full bg-slate-300 rounded-lg"
    />
    <table class="w-full table-auto" v-else>
      <thead>
        <th v-for="{ name, key } in columns" :key="key">{{ name }}</th>
      </thead>
      <tbody>
        <tr v-for="item in tableData" :key="item.id">
          <td v-for="{ key, type } in columns" :key="key">
            <p v-if="type === 'text'">{{ item[key] }}</p>
            <img
              v-else-if="type === 'data-url'"
              :src="`data:${item.image_type};base64,${item[key]}`"
              :alt="key"
            />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped lang="scss">
table {
  thead {
    @apply border-b;
    @apply border-slate-900;
  }

  tbody {
    tr {
      @apply border-b;
      @apply border-slate-300;

      td {
        @apply p-3;
        @apply text-center;

        img {
          @apply h-32;
          @apply aspect-square;
          @apply object-cover;
        }
      }
    }
  }
}
</style>
