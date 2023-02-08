import { serverSupabaseClient } from "#supabase/server";

type InsertValues = {
  entry_image: string;
  converted_image: string;
  image_type: string;
  user_email: string;
};

export default defineEventHandler(async (event) => {
  const { entry_image, converted_image, image_type, user_email } =
    await readBody<InsertValues>(event);
  const client = serverSupabaseClient(event);
  const { error } = await client
    .from("pictures")
    .insert({ entry_image, converted_image, image_type, user_email });
  return { error };
});
