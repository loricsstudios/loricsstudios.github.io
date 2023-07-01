require 'csv'

module Jekyll
  module CSVConverter
    def csv_to_array(input)
      CSV.parse(input, headers: true).map(&:to_h)
    end
  end
end

Liquid::Template.register_filter(Jekyll::CSVConverter)
