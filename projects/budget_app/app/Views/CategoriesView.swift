import SwiftUI

struct CategoryRow: View {
    let category: Category
    /// Called when user confirms deletion
    let onDelete: (Category) -> Void
     /// Called when the row is tapped for editing
    let onEdit: (Category) -> Void
    
    @State private var isHovering = false
    @State private var showDeleteConfirmation = false
    
    var body: some View {
        HStack {
            Text(category.name)
            Spacer()
            // Show the delete button only on hover
            if isHovering || showDeleteConfirmation {
                Button {
                    showDeleteConfirmation = true
                } label: {
                    Image(systemName: "trash")
                }
                .buttonStyle(BorderlessButtonStyle())
                .alert(isPresented: $showDeleteConfirmation) {
                    Alert(
                        title: Text("Delete Category"),
                        message: Text("Are you sure you want to delete category: \(category.name)?"),
                        primaryButton: .destructive(Text("Delete")) {
                            onDelete(category)
                        },
                        secondaryButton: .cancel()
                    )
                }
            }
        }
        // Detect hover to toggle the trash button’s visibility
        .onHover { hovering in
            isHovering = hovering
        }
        // Adding an onTapGesture for editing the category
        .contentShape(Rectangle())
        .onTapGesture {
            onEdit(category)
        }
    }
}


struct CategoriesView: View {
    @ObservedObject var dataStore: DataStore
    @State private var isShowingCategoryDetail = false
    @State private var showErrorAlert = false
    @State private var errorMessage = ""
    @State private var selectedCategory: Category? = nil

    var body: some View {
        VStack {
            Text("Categories")
                .font(.largeTitle)
                .padding()

            List {
                ForEach(dataStore.categories) { category in
                    CategoryRow(
                        category: category,
                        onDelete: { categoryToDelete in
                            deleteCategory(category: categoryToDelete)
                        },
                        onEdit: { categoryToEdit in
                            selectedCategory = categoryToEdit
                            isShowingCategoryDetail = true
                        }
                    )
                }
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)
            
            Button("Add Category") {
                // Set selectedCategory to nil so the detail view works in add mode
                selectedCategory = nil
                isShowingCategoryDetail.toggle()
            }
            .padding()
        }
        .padding()
        .sheet(isPresented: $isShowingCategoryDetail) {
            CategoryDetailView(
                dataStore: dataStore,
                categoryToEdit: selectedCategory,
                onComplete: {
                    isShowingCategoryDetail = false
                }
            )
        }
        .alert(isPresented: $showErrorAlert) {
            Alert(title: Text("Error deleting category"),
                  message: Text(errorMessage),
                  dismissButton: .default(Text("OK")))
        }
    }

    private func deleteCategory(category: Category) {
        do {
            try dataStore.deleteCategory(category)
        } catch {
            // Handle the error gracefully in SwiftUI
            errorMessage = error.localizedDescription
            showErrorAlert = true
        }
    }
}

// New view that handles both adding and editing a category.
struct CategoryDetailView: View {
    @Environment(\.presentationMode) var presentationMode
    @ObservedObject var dataStore: DataStore
    /// If non-nil, we're editing an existing category.
    let categoryToEdit: Category?
    /// Called after successfully adding or updating a category.
    let onComplete: () -> Void

    @State private var categoryName: String = ""
    
    var body: some View {
        VStack {
            Form {
                Section(header: Text("Category Details").font(.headline)) {
                    TextField("Enter category name", text: $categoryName)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                        .padding(.vertical, 5)
                }
            }
            .padding()
            
            HStack {
                Button("Cancel") {
                    presentationMode.wrappedValue.dismiss()
                }
                Spacer()
                Button(action: {
                    saveCategory()
                }, label: {
                    Text(categoryToEdit == nil ? "Add Category" : "Edit Category")
                })
                .disabled(categoryName.trimmingCharacters(in: .whitespaces).isEmpty)
            }
            .padding([.horizontal, .bottom])
        }
        .frame(minWidth: 300, minHeight: 200)
        .navigationTitle(categoryToEdit == nil ? "Add Category" : "Edit Category")
        .onAppear {
            if let category = categoryToEdit {
                categoryName = category.name
            }
        }
    }
    
    private func saveCategory() {
        let trimmedName = categoryName.trimmingCharacters(in: .whitespaces)
        if let category = categoryToEdit {
            // Editing an existing category
            var updatedCategory = category
            updatedCategory.name = trimmedName
            do {
                try dataStore.updateCategory(updatedCategory)
                onComplete()
            } catch {
                print("Error updating category: \(error)")
            }
        } else {
            // Adding a new category
            let newCategory = Category(name: trimmedName)
            do {
                try dataStore.addCategory(newCategory)
                onComplete()
            } catch {
                print("Error saving category: \(error)")
            }
        }
    }
}
