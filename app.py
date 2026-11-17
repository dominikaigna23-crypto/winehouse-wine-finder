last_error = error
error_text = str(error).upper()

                temporary_error = (
                is_temporary = (
"503" in error_text
or "UNAVAILABLE" in error_text
                    or "RESOURCE_EXHAUSTED" in error_text
or "429" in error_text
                    or "RESOURCE_EXHAUSTED" in error_text
)

                if temporary_error and attempt < 2:
                if is_temporary and attempt < 2:

time.sleep(
2 * (attempt + 1)
)

continue

                raise error
                raise

if response is None:

@@ -812,8 +812,8 @@ def rank_with_ai(
if (
"503" in error_text
or "UNAVAILABLE" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
or "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
):

st.error(
