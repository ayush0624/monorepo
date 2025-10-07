import SwiftUI

struct TransactionsView: View {
    @ObservedObject var dataStore: DataStore

    var body: some View {
        VStack {
            Text("Transactions")
                .font(.largeTitle)
            // Placeholder for transaction list
            Text("Transactions will go here.")
                .padding()
        }
        .padding()
    }
} 