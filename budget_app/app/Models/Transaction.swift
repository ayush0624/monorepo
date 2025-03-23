import Foundation

enum TransactionType: String, Codable {
    case expense
    case income
}

struct Transaction: Identifiable, Codable {
    let id: UUID
    var title: String
    var amount: Double
    var date: Date
    var category: String
    var subcategory: String?
    var type: TransactionType
    
    init(
        id: UUID = UUID(),
        title: String,
        amount: Double,
        date: Date,
        category: String,
        subcategory: String? = nil,
        type: TransactionType
    ) {
        self.id = id
        self.title = title
        self.amount = amount
        self.date = date
        self.category = category
        self.subcategory = subcategory
        self.type = type
    }
} 