import SwiftUI

struct AddCategoryView: View {
    @Environment(\.presentationMode) var presentationMode
    @ObservedObject var dataStore: DataStore
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
                Button("Save") {
                    addCategory()
                }
                .disabled(categoryName.trimmingCharacters(in: .whitespaces).isEmpty)
            }
            .padding([.horizontal, .bottom])
        }
        .frame(minWidth: 300, minHeight: 200)
        .navigationTitle("Add Category") // This can help if you use a NavigationView in a container
    }
    
    private func addCategory() {
        let newCategory = Category(name: categoryName.trimmingCharacters(in: .whitespaces))
        do {
            try dataStore.addCategory(newCategory)
            presentationMode.wrappedValue.dismiss()
        } catch {
            print("Error saving category: \(error)")
        }
    }
}
