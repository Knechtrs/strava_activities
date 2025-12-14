# Activate renv on project load
source("renv/activate.R")

# Automatically restore renv
if (!requireNamespace("renv", quietly = TRUE)) install.packages("renv")
tryCatch(renv::restore(prompt = FALSE), error = function(e) message("renv restore skipped: ", e))

# # Source global helper functions
# global_fun_path <- "/Users/adminaccount/Library/CloudStorage/OneDrive-Charité-UniversitätsmedizinBerlin/Data_analysis/R_functions/R"
# if (dir.exists(global_fun_path)) {
#   sapply(list.files(global_fun_path, full.names = TRUE, pattern = "\\.R$", recursive = TRUE), source)
# }
