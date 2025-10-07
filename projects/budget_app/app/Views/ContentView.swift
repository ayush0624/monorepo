import SwiftUI

struct ContentView: View {
    @State private var selectedTab: Tab? = .transactions
    @StateObject private var dataStore: DataStore = DataStore()
    @State private var showErrorAlert = false
    @State private var showSuccessAlert = false
    
    enum Tab {
        case transactions
        case categories
        case reports
    }
    
    var body: some View {
        NavigationSplitView {
            // Sidebar
            List(selection: $selectedTab) {
                NavigationLink(value: Tab.transactions) {
                    Label("Transactions", systemImage: "list.bullet")
                }
                NavigationLink(value: Tab.categories) {
                    Label("Categories", systemImage: "folder")
                }
                NavigationLink(value: Tab.reports) {
                    Label("Reports", systemImage: "chart.bar")
                }
            }
            .navigationDestination(for: Tab.self) { tab in
                switch tab {
                case .transactions:
                    TransactionsView(dataStore: dataStore)
                case .categories:
                    CategoriesView(dataStore: dataStore)
                case .reports:
                    ReportsView(dataStore: dataStore)
                }
            }
            .listStyle(.sidebar)
            .navigationTitle("Budget App")
            .frame(minWidth: 200)
            .toolbar {
                ToolbarItem(placement: .navigation) {
                    Button {
                        // TODO: Implement "Add" action
                    } label: {
                        Label("Add", systemImage: "plus")
                    }
                }
            }
            // Error Alert
            .alert("Failed to initialize DataStore", isPresented: $showErrorAlert) {
                Button("OK", role: .cancel) {
                    // Terminate the app when the error alert is dismissed.
                    #if os(macOS)
                    NSApplication.shared.terminate(nil)
                    #else
                    exit(0)
                    #endif
                }
            }
            // Success Alert
            .alert("Successfully loaded DataStore", isPresented: $showSuccessAlert) {
                Button("OK", role: .cancel) { }
            }
            .onAppear {
                dataStore.initialize { success in
                    if success {
                        showSuccessAlert = true
                    } else {
                        showErrorAlert = true
                    }
                }
            }
        } detail: {
            // Detail pane
            switch selectedTab {
            case .transactions:
                TransactionsView(dataStore: dataStore)
            case .categories:
                CategoriesView(dataStore: dataStore)
            case .reports:
                ReportsView(dataStore: dataStore)
            case .none:
                Text("Select a tab")
                    .font(.title)
                    .foregroundColor(.secondary)
            }
        }
    }
}
