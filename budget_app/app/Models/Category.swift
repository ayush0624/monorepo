import Foundation

struct Category: Identifiable, Codable {
    let id: UUID
    var name: String
    var subcategories: [String]
    
    init(id: UUID = UUID(), name: String, subcategories: [String] = []) {
        self.id = id
        self.name = name
        self.subcategories = subcategories
    }
} 